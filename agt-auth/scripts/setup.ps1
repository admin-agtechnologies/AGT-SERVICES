# AGT Auth Service v1.0 - Setup (Windows PowerShell)

Write-Host "AGT Auth Service v1.0 - Setup" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

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
    Write-Host "  -> Puis relancez ce script." -ForegroundColor Yellow
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

# 2. Cles RSA
if (-not (Test-Path "keys\private.pem")) {
    New-Item -ItemType Directory -Path "keys" -Force | Out-Null

    $hasOpenssl = $null -ne (Get-Command openssl -ErrorAction SilentlyContinue)

    if ($hasOpenssl) {
        Write-Host "[INFO] OpenSSL detecte, generation locale..." -ForegroundColor Cyan
        openssl genrsa -out keys\private.pem 2048
        openssl rsa -in keys\private.pem -pubout -out keys\public.pem
    }
    else {
        Write-Host "[INFO] OpenSSL absent, generation via Docker..." -ForegroundColor Cyan
        docker run --rm -v "${PWD}\keys:/keys" alpine/openssl genrsa -out /keys/private.pem 2048
        docker run --rm -v "${PWD}\keys:/keys" alpine/openssl rsa -in /keys/private.pem -pubout -out /keys/public.pem
    }

    if (Test-Path "keys\private.pem") {
        Write-Host "[OK] Cles RSA generees dans keys\" -ForegroundColor Green
    }
    else {
        Write-Host "[ERREUR] Echec generation des cles RSA" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "[INFO] Cles RSA existent deja" -ForegroundColor Yellow
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
docker compose exec auth python manage.py migrate --noinput

# 6. Health check
Write-Host ""
Write-Host "Health check..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:7000/api/v1/auth/health" -Method GET
    $health | ConvertTo-Json
}
catch {
    Write-Host "Service en cours de demarrage, reessayez dans quelques secondes..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[OK] Auth Service pret sur http://localhost:7000" -ForegroundColor Green
Write-Host ""
Write-Host "Documentation API :" -ForegroundColor Cyan
Write-Host "  Swagger UI : http://localhost:7000/api/v1/docs/" -ForegroundColor Gray
Write-Host "  ReDoc      : http://localhost:7000/api/v1/redoc/" -ForegroundColor Gray
Write-Host ""
Write-Host "Tests : docker compose exec auth python -m pytest -v" -ForegroundColor Gray
