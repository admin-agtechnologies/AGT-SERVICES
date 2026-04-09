# AGT Users Service v1.0 - Setup (Windows PowerShell)

Write-Host "AGT Users Service v1.0 - Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 0. Verifier Docker
$dockerOk = $false
try {
    $null = docker info 2>$null
    $dockerOk = $true
}
catch {}

if (-not $dockerOk) {
    Write-Host "[ERREUR] Docker n'est pas accessible." -ForegroundColor Red
    Write-Host "  -> Ouvrez Docker Desktop et attendez qu'il soit pret (icone verte)." -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Docker actif" -ForegroundColor Green

# 1. .env
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] .env cree depuis .env.example" -ForegroundColor Green
}
else {
    Write-Host "[INFO] .env existe deja" -ForegroundColor Yellow
}

# 2. Cle publique Auth
if (-not (Test-Path "keys\auth_public.pem")) {
    New-Item -ItemType Directory -Path "keys" -Force | Out-Null

    if (Test-Path "..\agt-auth\keys\public.pem") {
        Copy-Item "..\agt-auth\keys\public.pem" "keys\auth_public.pem"
        Write-Host "[OK] Cle publique Auth copiee depuis ..\agt-auth\keys\" -ForegroundColor Green
    }
    else {
        Write-Host "[WARN] Cle publique Auth introuvable dans ..\agt-auth\keys\public.pem" -ForegroundColor Yellow
        Write-Host "       Copiez-la manuellement : copy <chemin>\public.pem keys\auth_public.pem" -ForegroundColor Yellow
    }
}
else {
    Write-Host "[INFO] Cle publique Auth existe deja" -ForegroundColor Yellow
}

# 3. Build et Start
Write-Host ""
Write-Host "Build et demarrage Docker..." -ForegroundColor Cyan
docker compose up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERREUR] Docker compose a echoue" -ForegroundColor Red
    exit 1
}

# 4. Attente
Write-Host "Attente demarrage services..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# 5. Migrations
Write-Host "Migrations..." -ForegroundColor Cyan
docker compose exec users python manage.py migrate --noinput

# 6. Health check
Write-Host ""
Write-Host "Health check..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:7001/api/v1/health" -Method GET
    $health | ConvertTo-Json
}
catch {
    Write-Host "Service en cours de demarrage, reessayez dans quelques secondes..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[OK] Users Service pret sur http://localhost:7001" -ForegroundColor Green
Write-Host ""
Write-Host "Documentation API :" -ForegroundColor Cyan
Write-Host "  Swagger UI : http://localhost:7001/api/v1/docs/" -ForegroundColor Gray
Write-Host "  ReDoc      : http://localhost:7001/api/v1/redoc/" -ForegroundColor Gray
Write-Host ""
Write-Host "Tests : docker compose exec users python -m pytest -v" -ForegroundColor Gray
