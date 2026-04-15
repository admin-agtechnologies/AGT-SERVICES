# =========================================
#  STOP & CLEAN - AG TECHNOLOGIES
#  Arrete et supprime TOUT sans redéployer
#  Usage : .\stop_clean.ps1
# =========================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Red
Write-Host " STOP & CLEAN - AG TECHNOLOGIES          " -ForegroundColor Red
Write-Host " TOUS les services seront arretes et     " -ForegroundColor Red
Write-Host " supprimes (containers, volumes, reseau) " -ForegroundColor Red
Write-Host "=========================================" -ForegroundColor Red
Write-Host ""

# --- Confirmation interactive ---
$confirm = Read-Host "Es-tu sur de vouloir tout supprimer ? (oui/non)"
if ($confirm -ne "oui") {
    Write-Host ""
    Write-Host " -> Annule. Aucune modification effectuee." -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# =========================================
# LISTE DE TOUS LES SERVICES AGT
# =========================================

# Services metier (docker-compose par dossier)
$services = @(
    "agt-auth",
    "agt-users",
    "agt-notification",
    "agt-subscription",
    "agt-payment",
    "agt-wallet",
    "agt-search",
    "agt-chatbot",
    "agt-chat",
    "agt-media",
    "agt-geoloc"
)

# Containers de l'infrastructure partagee (docker-compose.infra.yml)
$infraContainers = @(
    "agt-gateway",
    "agt-rabbitmq",
    "agt-elasticsearch",
    "agt-mailpit"
)

# =========================================
# [1/5] ARRET ET SUPPRESSION DES SERVICES
# =========================================

Write-Host "[1/5] Arret des services AGT..." -ForegroundColor Cyan

foreach ($svc in $services) {
    $composePath = ".\$svc\docker-compose.yml"
    if (Test-Path $composePath) {
        Write-Host " -> Arret de $svc..." -ForegroundColor Gray
        docker compose -f $composePath down --remove-orphans 2>$null
    }
}

# =========================================
# [2/5] ARRET DE L'INFRASTRUCTURE PARTAGEE
# =========================================

Write-Host ""
Write-Host "[2/5] Arret de l'infrastructure partagee..." -ForegroundColor Cyan

if (Test-Path ".\docker-compose.infra.yml") {
    Write-Host " -> Arret de gateway, rabbitmq, elasticsearch, mailpit..." -ForegroundColor Gray
    docker compose -f docker-compose.infra.yml down --remove-orphans 2>$null
}

# =========================================
# [3/5] SUPPRESSION DES VOLUMES AGT
# =========================================

Write-Host ""
Write-Host "[3/5] Suppression des volumes AGT..." -ForegroundColor Cyan

$volumes = docker volume ls --format "{{.Name}}" 2>$null | Where-Object { $_ -match "^agt" }

if ($volumes.Count -gt 0) {
    foreach ($vol in $volumes) {
        Write-Host " -> Suppression volume : $vol" -ForegroundColor Gray
        docker volume rm $vol 2>$null
    }
    Write-Host " -> $($volumes.Count) volume(s) supprime(s)." -ForegroundColor Green
} else {
    Write-Host " -> Aucun volume AGT trouve." -ForegroundColor Gray
}

# =========================================
# [4/5] SUPPRESSION DU RESEAU AGT
# =========================================

Write-Host ""
Write-Host "[4/5] Suppression du reseau agt_network..." -ForegroundColor Cyan

$network = docker network ls --format "{{.Name}}" 2>$null | Where-Object { $_ -eq "agt_network" }
if ($network) {
    docker network rm agt_network 2>$null
    Write-Host " -> Reseau agt_network supprime." -ForegroundColor Green
} else {
    Write-Host " -> Reseau agt_network introuvable (deja supprime)." -ForegroundColor Gray
}

# =========================================
# [5/5] SUPPRESSION DES FICHIERS .env
# =========================================

Write-Host ""
Write-Host "[5/5] Suppression des fichiers .env..." -ForegroundColor Cyan

$envCount = 0
foreach ($svc in $services) {
    $envPath = ".\$svc\.env"
    if (Test-Path $envPath) {
        Remove-Item $envPath -Force
        Write-Host " -> $svc\.env supprime." -ForegroundColor Gray
        $envCount++
    }
}

if ($envCount -eq 0) {
    Write-Host " -> Aucun fichier .env trouve." -ForegroundColor Gray
} else {
    Write-Host " -> $envCount fichier(s) .env supprime(s)." -ForegroundColor Green
}

# =========================================
# VERIFICATION FINALE
# =========================================

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " NETTOYAGE TERMINE                       " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host " Verification - containers actifs :" -ForegroundColor White
Write-Host ""

$remaining = docker ps --format "{{.Names}}" 2>$null | Where-Object { $_ -match "^agt" }

if ($remaining.Count -gt 0) {
    Write-Host " /!\ Containers AGT encore actifs :" -ForegroundColor Yellow
    foreach ($c in $remaining) {
        Write-Host "     - $c" -ForegroundColor Yellow
    }
} else {
    Write-Host " -> Aucun container AGT actif. Tout est propre." -ForegroundColor Green
}

Write-Host ""
docker ps
Write-Host ""
Write-Host " Pour relancer le MVP :" -ForegroundColor Cyan
Write-Host "   .\deploy_mvp.ps1" -ForegroundColor White
Write-Host ""
Write-Host " Pour relancer tous les services :" -ForegroundColor Cyan
Write-Host "   .\deploy_all.ps1" -ForegroundColor White
Write-Host ""