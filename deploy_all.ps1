# =============================================================================
# AG TECHNOLOGIES — DÉPLOIEMENT COMPLET (Windows PowerShell)
# Tous les 11 services + infrastructure partagée
# =============================================================================

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " DÉPLOIEMENT COMPLET - AG TECHNOLOGIES   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# --- Fonction utilitaire : attendre qu'un service soit healthy ---
function Wait-ForHealthCheck {
    param(
        [string]$ServiceName,
        [string]$Url,
        [int]$MaxAttempts = 30,
        [int]$DelaySeconds = 2
    )
    Write-Host " -> Attente de $ServiceName..." -ForegroundColor DarkGray
    for ($i = 1; $i -le $MaxAttempts; $i++) {
        try {
            $response = Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 3 -ErrorAction Stop
            Write-Host " -> $ServiceName est prêt ! ($i tentative(s))" -ForegroundColor Green
            return $true
        } catch {
            Start-Sleep -Seconds $DelaySeconds
        }
    }
    Write-Host " -> ATTENTION: $ServiceName n'a pas répondu après $($MaxAttempts * $DelaySeconds)s" -ForegroundColor Yellow
    return $false
}

# --- Étape 1 : Création du réseau + Infrastructure partagée ---
Write-Host "`n[1/6] Lancement de l'infrastructure partagée..." -ForegroundColor Yellow

$networkExists = docker network ls --filter name=^agt_network$ --format "{{.Name}}" 2>$null
if (-not $networkExists) {
    docker network create agt_network | Out-Null
    Write-Host " -> Réseau agt_network créé." -ForegroundColor DarkGray
}

docker compose -f docker-compose.infra.yml up -d
Write-Host " -> Infrastructure lancée." -ForegroundColor Green

# --- Étape 2 : Simulateurs (Média, Chat, Geoloc) ---
Write-Host "`n[2/6] Lancement des simulateurs..." -ForegroundColor Yellow
$simulators = @("agt-media", "agt-chat", "agt-geoloc")
foreach ($sim in $simulators) {
    if (Test-Path $sim) {
        Write-Host " -> Démarrage de $sim..." -ForegroundColor DarkGray
        cd $sim
        docker compose up -d --build
        cd ..
    } else {
        Write-Host " -> $sim non trouvé, ignoré." -ForegroundColor Yellow
    }
}

# --- Étape 3 : Auth + Health Check ---
Write-Host "`n[3/6] Lancement du Service Auth..." -ForegroundColor Yellow
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
cd ..

$authOk = Wait-ForHealthCheck -ServiceName "Auth" -Url "http://localhost:7000/api/v1/auth/health"
if (-not $authOk) {
    Write-Host "`nDÉPLOIEMENT INTERROMPU : Auth n'a pas démarré." -ForegroundColor Red
    exit 1
}

# --- Étape 4 : Distribution de la clé publique Auth ---
Write-Host "`n[4/6] Partage de la clé publique Auth vers tous les services..." -ForegroundColor Yellow
$authPubKey = "agt-auth\keys\public.pem"
$targetServices = @("agt-users", "agt-notification", "agt-subscription", "agt-payment", "agt-wallet", "agt-search", "agt-chatbot")

if (Test-Path $authPubKey) {
    foreach ($service in $targetServices) {
        if (Test-Path $service) {
            New-Item -ItemType Directory -Force -Path "$service\keys" | Out-Null
            Copy-Item -Path $authPubKey -Destination "$service\keys\auth_public.pem" -Force
            Write-Host " -> Clé copiée vers $service." -ForegroundColor DarkGray
        }
    }
    Write-Host " -> Toutes les clés distribuées." -ForegroundColor Green
} else {
    Write-Host " -> ERREUR: Clé publique Auth introuvable !" -ForegroundColor Red
    exit 1
}

# --- Étape 5 : Lancement des services métier (dans l'ordre des dépendances) ---
Write-Host "`n[5/6] Lancement des services métier..." -ForegroundColor Yellow
foreach ($service in $targetServices) {
    if (Test-Path "$service\scripts\setup.ps1") {
        Write-Host " -> Démarrage de $service..." -ForegroundColor DarkGray
        cd $service
        .\scripts\setup.ps1
        cd ..
    } else {
        Write-Host " -> $service : script setup non trouvé, ignoré." -ForegroundColor Yellow
    }
}

# --- Étape 6 : Health Checks finaux ---
Write-Host "`n[6/6] Vérification de santé de tous les services..." -ForegroundColor Yellow

$healthChecks = @(
    @{ Name = "Auth";         Url = "http://localhost:7000/api/v1/auth/health" },
    @{ Name = "Users";        Url = "http://localhost:7001/api/v1/health" },
    @{ Name = "Notification"; Url = "http://localhost:7002/api/v1/health" },
    @{ Name = "Subscription"; Url = "http://localhost:7004/api/v1/subscriptions/health" },
    @{ Name = "Payment";      Url = "http://localhost:7005/api/v1/payments/health" },
    @{ Name = "Wallet";       Url = "http://localhost:7006/api/v1/wallet/health" },
    @{ Name = "Search";       Url = "http://localhost:7007/api/v1/search/health" },
    @{ Name = "Chatbot";      Url = "http://localhost:7010/api/v1/chatbot/health" }
)

$allOk = $true
foreach ($check in $healthChecks) {
    $ok = Wait-ForHealthCheck -ServiceName $check.Name -Url $check.Url -MaxAttempts 15 -DelaySeconds 2
    if (-not $ok) { $allOk = $false }
}

# --- Résumé final ---
Write-Host "`n=========================================" -ForegroundColor Cyan
if ($allOk) {
    Write-Host " DÉPLOIEMENT COMPLET RÉUSSI !            " -ForegroundColor Green
} else {
    Write-Host " DÉPLOIEMENT PARTIEL (certains services KO)" -ForegroundColor Yellow
}
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " Vérifiez l'état : docker ps" -ForegroundColor Gray
Write-Host " Reset soft       : .\reset_all.ps1" -ForegroundColor Gray
Write-Host " Reset complet    : .\reset_all.ps1 --clean" -ForegroundColor Gray
Write-Host "=========================================" -ForegroundColor Cyan