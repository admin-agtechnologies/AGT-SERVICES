# =============================================================================
# AG TECHNOLOGIES — DÉPLOIEMENT MVP (Windows PowerShell)
# Services : Auth (7000) + Users (7001) + Notification (7002)
# Infra    : Gateway, RabbitMQ, Mailpit, Elasticsearch
# =============================================================================

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " DÉPLOIEMENT MVP - AG TECHNOLOGIES       " -ForegroundColor Cyan
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
    Write-Host " -> ERREUR: $ServiceName n'a pas répondu après $($MaxAttempts * $DelaySeconds)s !" -ForegroundColor Red
    Write-Host "   Vérifiez les logs : docker logs <container_name>" -ForegroundColor Red
    return $false
}

# --- Étape 1 : Création du réseau + Infrastructure partagée ---
Write-Host "`n[1/4] Lancement de l'infrastructure partagée..." -ForegroundColor Yellow

# Créer le réseau s'il n'existe pas
$networkExists = docker network ls --filter name=^agt_network$ --format "{{.Name}}" 2>$null
if (-not $networkExists) {
    docker network create agt_network | Out-Null
    Write-Host " -> Réseau agt_network créé." -ForegroundColor DarkGray
}

docker compose -f docker-compose.infra.yml up -d
Write-Host " -> Infrastructure lancée (Gateway, RabbitMQ, Mailpit, Elasticsearch)." -ForegroundColor Green

# --- Étape 2 : Lancement de Auth + Health Check ---
Write-Host "`n[2/4] Lancement du Service Auth..." -ForegroundColor Yellow
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
cd ..

$authOk = Wait-ForHealthCheck -ServiceName "Auth" -Url "http://localhost:7000/api/v1/auth/health"
if (-not $authOk) {
    Write-Host "`nDÉPLOIEMENT INTERROMPU : Auth n'a pas démarré." -ForegroundColor Red
    exit 1
}

# --- Étape 3 : Copie de la clé publique Auth ---
Write-Host "`n[3/4] Partage de la clé publique Auth..." -ForegroundColor Yellow
$authPubKey = "agt-auth\keys\public.pem"
if (Test-Path $authPubKey) {
    # Users
    New-Item -ItemType Directory -Force -Path "agt-users\keys" | Out-Null
    Copy-Item -Path $authPubKey -Destination "agt-users\keys\auth_public.pem" -Force
    Write-Host " -> Clé copiée vers agt-users." -ForegroundColor DarkGray

    # Notification
    New-Item -ItemType Directory -Force -Path "agt-notification\keys" | Out-Null
    Copy-Item -Path $authPubKey -Destination "agt-notification\keys\auth_public.pem" -Force
    Write-Host " -> Clé copiée vers agt-notification." -ForegroundColor DarkGray

    Write-Host " -> Clés distribuées avec succès." -ForegroundColor Green
} else {
    Write-Host " -> ERREUR: Clé publique Auth introuvable ($authPubKey) !" -ForegroundColor Red
    Write-Host "   Le service Auth a-t-il bien généré ses clés ?" -ForegroundColor Red
    exit 1
}

# --- Étape 4 : Lancement de Users + Notification + Health Checks ---
Write-Host "`n[4/4] Lancement des Services Users et Notification..." -ForegroundColor Yellow

cd agt-users
.\scripts\setup.ps1
cd ..

cd agt-notification
.\scripts\setup.ps1
cd ..

$usersOk = Wait-ForHealthCheck -ServiceName "Users" -Url "http://localhost:7001/api/v1/health"
$notifOk = Wait-ForHealthCheck -ServiceName "Notification" -Url "http://localhost:7002/api/v1/health"

# --- Résumé final ---
Write-Host "`n=========================================" -ForegroundColor Cyan
if ($authOk -and $usersOk -and $notifOk) {
    Write-Host " DÉPLOIEMENT MVP RÉUSSI !                " -ForegroundColor Green
} else {
    Write-Host " DÉPLOIEMENT MVP PARTIEL (erreurs)       " -ForegroundColor Yellow
}
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host " Services :" -ForegroundColor White
Write-Host "   Auth         : http://localhost:7000/api/v1/docs/" -ForegroundColor Gray
Write-Host "   Users        : http://localhost:7001/api/v1/docs/" -ForegroundColor Gray
Write-Host "   Notification : http://localhost:7002/api/v1/docs/" -ForegroundColor Gray
Write-Host ""
Write-Host " Outils :" -ForegroundColor White
Write-Host "   Mailpit      : http://localhost:8025" -ForegroundColor Gray
Write-Host "   RabbitMQ     : http://localhost:15672 (agt_rabbit / agt_rabbit_password)" -ForegroundColor Gray
Write-Host ""
Write-Host " Commandes utiles :" -ForegroundColor White
Write-Host "   docker ps                    → voir les conteneurs" -ForegroundColor Gray
Write-Host "   .\reset_mvp.ps1             → reset soft (garde les données)" -ForegroundColor Gray
Write-Host "   .\reset_mvp.ps1 --clean     → reset complet (supprime tout)" -ForegroundColor Gray
Write-Host "=========================================" -ForegroundColor Cyan