# =============================================================================
# AG TECHNOLOGIES — RESET MVP (Windows PowerShell)
# Usage : .\reset_mvp.ps1           → reset sans perte de données
#         .\reset_mvp.ps1 --clean   → reset + suppression des volumes (données)
# =============================================================================

param(
    [switch]$clean
)

# Détection du flag --clean passé en argument positionnel
if ($args -contains "--clean") { $clean = $true }

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " RESET MVP - AG TECHNOLOGIES             " -ForegroundColor Cyan
if ($clean) {
    Write-Host " MODE: CLEAN (volumes seront supprimés)  " -ForegroundColor Red
} else {
    Write-Host " MODE: SOFT (volumes conservés)          " -ForegroundColor Green
}
Write-Host "=========================================" -ForegroundColor Cyan

# --- Conteneurs ciblés MVP ---
# Auth, Users, Notification + Infra (gateway, rabbitmq, mailpit, elasticsearch)
$mvpPatterns = @("agt_auth_", "agt_users_", "agt_notif_", "agt-gateway", "agt-rabbitmq", "agt-mailpit", "agt-elasticsearch")

# --- Étape 1 : Arrêt et suppression des conteneurs AGT MVP ---
Write-Host "`n[1/5] Arrêt des conteneurs AGT MVP..." -ForegroundColor Yellow
$allContainers = docker ps -a --format "{{.Names}}"
$toStop = @()
foreach ($container in $allContainers) {
    foreach ($pattern in $mvpPatterns) {
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
    Write-Host " -> Aucun conteneur MVP trouvé." -ForegroundColor DarkGray
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

# --- Étape 3 : Suppression des fichiers .env MVP ---
Write-Host "`n[3/5] Suppression des fichiers .env MVP..." -ForegroundColor Yellow
$envFiles = @("agt-auth\.env", "agt-users\.env", "agt-notification\.env")
foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        Remove-Item -Path $envFile -Force
        Write-Host " -> $envFile supprimé." -ForegroundColor DarkGray
    }
}
Write-Host " -> Fichiers .env nettoyés." -ForegroundColor Green

# --- Étape 4 : Suppression des volumes (uniquement si --clean) ---
Write-Host "`n[4/5] Gestion des volumes..." -ForegroundColor Yellow
if ($clean) {
    Write-Host " -> Mode --clean : suppression des volumes AGT MVP..." -ForegroundColor Red

    # Volumes créés par docker-compose dans chaque service (préfixe = nom du dossier)
    $volumePatterns = @("agt-auth_", "agt-users_", "agt-notification_")
    # Volumes de l'infra partagée (nom du dossier racine + nom du volume)
    # Le préfixe dépend du nom du dossier parent du docker-compose.infra.yml

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
        # Volumes infra (rabbitmq_data, es_data créés par le compose infra)
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

# --- Étape 5 : Relancement du MVP ---
Write-Host "`n[5/5] Relancement du déploiement MVP..." -ForegroundColor Yellow
.\deploy_mvp.ps1