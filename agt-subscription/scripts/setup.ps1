# AGT Subscription Service v1.0 - Setup (Windows PowerShell)
Write-Host "AGT Subscription Service v1.0 - Setup" -ForegroundColor Cyan
$dockerOk = $false
try { $null = docker info 2>$null; $dockerOk = $true } catch {}
if (-not $dockerOk) { Write-Host "[ERREUR] Ouvrez Docker Desktop." -ForegroundColor Red; exit 1 }
Write-Host "[OK] Docker actif" -ForegroundColor Green
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "[OK] .env cree" -ForegroundColor Green }
if (-not (Test-Path "keys\auth_public.pem")) {
    New-Item -ItemType Directory -Path "keys" -Force | Out-Null
    if (Test-Path "..\agt-auth\keys\public.pem") { Copy-Item "..\agt-auth\keys\public.pem" "keys\auth_public.pem"; Write-Host "[OK] Cle Auth copiee" -ForegroundColor Green }
    else { Write-Host "[WARN] Cle Auth introuvable" -ForegroundColor Yellow }
}
Write-Host "Build et demarrage Docker..." -ForegroundColor Cyan
docker compose up -d --build
Start-Sleep -Seconds 8
Write-Host "Migrations..." -ForegroundColor Cyan
docker compose exec subscription python manage.py migrate --noinput
Write-Host ""
try { $h = Invoke-RestMethod -Uri "http://localhost:7004/api/v1/subscriptions/health"; $h | ConvertTo-Json } catch { Write-Host "En cours de demarrage..." -ForegroundColor Yellow }
Write-Host ""
Write-Host "[OK] Subscription Service pret sur http://localhost:7004" -ForegroundColor Green
Write-Host "  Swagger : http://localhost:7004/api/v1/docs/" -ForegroundColor Gray
Write-Host "  Tests   : docker compose exec subscription python -m pytest -v" -ForegroundColor Gray
