# Sync memory files + any code changes, then push to GitHub.
# After pushing, marks all unsynced Team Updates in Supabase as processed.
# Usage: .\sync.ps1
# Or with a custom commit message: .\sync.ps1 "Updated after Sep 3 call"

param([string]$Message = "Update dashboard")

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

# ── Step 1: Copy memory files ──

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

# ── Step 2: Check for any changes (data + code) ──

$dataChanges = git diff --stat HEAD -- data/memory/
$codeStatus = git status --porcelain -- "*.py" "*.txt" "*.toml" "pages/" "*.ps1" | Where-Object { $_ -notmatch "secrets\.toml" }

$hasData = [bool]$dataChanges
$hasCode = [bool]$codeStatus

if (-not $hasData -and -not $hasCode) {
    Write-Host "`nNo changes detected. Nothing to push." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
if ($hasData) {
    Write-Host "Data changes:" -ForegroundColor Cyan
    git diff --stat HEAD -- data/memory/
}
if ($hasCode) {
    Write-Host "Code changes:" -ForegroundColor Cyan
    $codeStatus | ForEach-Object { Write-Host "  $_" -ForegroundColor Green }
}

# ── Step 3: Stage, commit, push ──

$ErrorActionPreference = "Continue"

git add data/memory/
if ($hasCode) {
    git add *.py pages/*.py requirements.txt nav.py sync.ps1
    git add *.py
}

$ErrorActionPreference = "Stop"

git commit -m $Message
git push

# ── Step 4: Mark team updates as processed in Supabase ──

Write-Host "`nMarking team updates as synced..." -ForegroundColor Cyan
$secretsPath = Join-Path $PSScriptRoot ".streamlit\secrets.toml"
if (Test-Path $secretsPath) {
    $secretsContent = Get-Content $secretsPath -Raw
    $supabaseUrl = ([regex]::Match($secretsContent, 'supabase_url\s*=\s*"([^"]+)"')).Groups[1].Value
    $supabaseKey = ([regex]::Match($secretsContent, 'supabase_key\s*=\s*"([^"]+)"')).Groups[1].Value

    if ($supabaseUrl -and $supabaseKey) {
        $headers = @{
            "apikey"        = $supabaseKey
            "Authorization" = "Bearer $supabaseKey"
            "Content-Type"  = "application/json"
            "Prefer"        = "return=representation"
        }
        $body = '{"synced_at":"' + (Get-Date -Format "o") + '"}'
        $uri = "$supabaseUrl/rest/v1/workstream_notes?synced_at=is.null"
        try {
            $result = Invoke-RestMethod -Uri $uri -Method PATCH -Headers $headers -Body $body
            $count = @($result).Count
            Write-Host "  Marked $count team update(s) as processed." -ForegroundColor Green
        } catch {
            Write-Host "  Warning: Could not mark updates as synced: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Skipped (Supabase credentials not found in secrets.toml)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Skipped (secrets.toml not found)" -ForegroundColor Yellow
}

Write-Host "`nDone! Dashboard will auto-redeploy in ~1 minute." -ForegroundColor Green
