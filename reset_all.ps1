# =============================================================================
# AG TECHNOLOGIES — RESET ALL (Windows PowerShell)
# Usage : .\reset_all.ps1           → reset sans perte de données
#         .\reset_all.ps1 --clean   → reset + suppression des volumes (données)
# =============================================================================

param(
    [switch]$clean
)

# Détection du flag --clean passé en argument positionnel
if ($args -contains "--clean") { $clean = $true }

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " RESET ALL - AG TECHNOLOGIES             " -ForegroundColor Cyan
if ($clean) {
    Write-Host " MODE: CLEAN (volumes seront supprimés)  " -ForegroundColor Red
} else {
    Write-Host " MODE: SOFT (volumes conservés)          " -ForegroundColor Green
}
Write-Host "=========================================" -ForegroundColor Cyan

# --- Tous les conteneurs AGT (11 services + infra) ---
$allPatterns = @(
    "agt_auth_", "agt_users_", "agt_notif_",
    "agt_sub_", "agt_pay_", "agt_wallet_",
    "agt_search_", "agt_chatbot_",
    "agt_media_", "agt_chat_", "agt_geoloc_",
    "agt_gateway", "agt_rabbitmq", "agt_mailpit", "agt_elasticsearch"
)

# --- Étape 1 : Arrêt et suppression des conteneurs AGT ---
Write-Host "`n[1/5] Arrêt de tous les conteneurs AGT..." -ForegroundColor Yellow
$allContainers = docker ps -a --format "{{.Names}}"
$toStop = @()
foreach ($container in $allContainers) {
    foreach ($pattern in $allPatterns) {
        if ($container -like "$pattern*") {
            $toStop += $container
            break
        }
    }
}

if ($toStop.Count -gt 0) {
    foreach ($c in $toStop) {
        Write-Host " -> Arrêt de $c..." -ForegroundColor DarkGray
        docker stop $c 2>$null | Out-Null
        docker rm $c 2>$null | Out-Null
    }
    Write-Host " -> $($toStop.Count) conteneur(s) supprimé(s)." -ForegroundColor Green
} else {
    Write-Host " -> Aucun conteneur AGT trouvé." -ForegroundColor DarkGray
}

# --- Étape 2 : Suppression du réseau AGT ---
Write-Host "`n[2/5] Suppression du réseau agt_network..." -ForegroundColor Yellow
$networkExists = docker network ls --filter name=^agt_network$ --format "{{.Name}}" 2>$null
if ($networkExists) {
    docker network rm agt_network 2>$null | Out-Null
    Write-Host " -> Réseau supprimé." -ForegroundColor Green
} else {
    Write-Host " -> Réseau inexistant, rien à faire." -ForegroundColor DarkGray
}

# --- Étape 3 : Suppression des fichiers .env (tous les services) ---
Write-Host "`n[3/5] Suppression des fichiers .env..." -ForegroundColor Yellow
$services = @(
    "agt-auth", "agt-users", "agt-notification",
    "agt-subscription", "agt-payment", "agt-wallet",
    "agt-search", "agt-chatbot",
    "agt-media", "agt-chat", "agt-geoloc"
)
foreach ($service in $services) {
    $envPath = "$service\.env"
    if (Test-Path $envPath) {
        Remove-Item -Path $envPath -Force
        Write-Host " -> $envPath supprimé." -ForegroundColor DarkGray
    }
}
Write-Host " -> Fichiers .env nettoyés." -ForegroundColor Green

# --- Étape 4 : Suppression des volumes (uniquement si --clean) ---
Write-Host "`n[4/5] Gestion des volumes..." -ForegroundColor Yellow
if ($clean) {
    Write-Host " -> Mode --clean : suppression de tous les volumes AGT..." -ForegroundColor Red

    $volumePatterns = @(
        "agt-auth_", "agt-users_", "agt-notification_",
        "agt-subscription_", "agt-payment_", "agt-wallet_",
        "agt-search_", "agt-chatbot_",
        "agt-media_", "agt-chat_", "agt-geoloc_"
    )

    $allVolumes = docker volume ls --format "{{.Name}}"
    $deletedCount = 0
    foreach ($vol in $allVolumes) {
        foreach ($pattern in $volumePatterns) {
            if ($vol -like "$pattern*") {
                docker volume rm $vol 2>$null | Out-Null
                Write-Host "    -> Volume $vol supprimé." -ForegroundColor DarkGray
                $deletedCount++
                break
            }
        }
        # Volumes infra
        if ($vol -match "rabbitmq_data|es_data") {
            docker volume rm $vol 2>$null | Out-Null
            Write-Host "    -> Volume $vol supprimé." -ForegroundColor DarkGray
            $deletedCount++
        }
    }
    Write-Host " -> $deletedCount volume(s) supprimé(s)." -ForegroundColor Green
} else {
    Write-Host " -> Mode soft : volumes conservés (données intactes)." -ForegroundColor Green
}

# --- Étape 5 : Relancement complet ---
Write-Host "`n[5/5] Relancement du déploiement complet..." -ForegroundColor Yellow
.\deploy_all.ps1