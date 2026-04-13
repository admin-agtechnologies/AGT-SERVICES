# deploy_all.ps1
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " DÉPLOIEMENT COMPLET - AG TECHNOLOGIES   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Infra partagée
Write-Host "`n[1/5] Lancement de l'infrastructure partagée (Gateway, RabbitMQ, ES)..." -ForegroundColor Yellow
docker compose -f "Docker compose.infra.yml" up -d

# 2. Simulateurs
Write-Host "`n[2/5] Lancement des simulateurs (Media, Chat, Geoloc)..." -ForegroundColor Yellow
$simulators = @("agt-media", "agt-chat", "agt-geoloc")
foreach ($sim in $simulators) {
    Write-Host " -> Démarrage de $sim..." -ForegroundColor DarkGray
    cd $sim
    docker compose up -d --build
    cd ..
}

# 3. Auth
Write-Host "`n[3/5] Lancement du Service Auth (Génération des clés RSA)..." -ForegroundColor Yellow
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
cd ..

Write-Host "Attente de la génération des clés..." -ForegroundColor DarkGray
Start-Sleep -Seconds 5

# 4. Partage des clés
Write-Host "`n[4/5] Partage de la clé publique Auth vers tous les services..." -ForegroundColor Yellow
$authPubKey = "agt-auth\keys\public.pem"
$targetServices = @("agt-users", "agt-notification", "agt-subscription", "agt-payment", "agt-wallet", "agt-search", "agt-chatbot")

if (Test-Path $authPubKey) {
    foreach ($service in $targetServices) {
        New-Item -ItemType Directory -Force -Path "$service\keys" | Out-Null
        Copy-Item -Path $authPubKey -Destination "$service\keys\auth_public.pem" -Force
        Write-Host " -> Clé copiée vers $service" -ForegroundColor DarkGray
    }
    Write-Host "Toutes les clés ont été distribuées." -ForegroundColor Green
} else {
    Write-Host "ATTENTION: Clé publique Auth introuvable !" -ForegroundColor Red
}

# 5. Autres services
Write-Host "`n[5/5] Lancement des services métier restants..." -ForegroundColor Yellow
foreach ($service in $targetServices) {
    Write-Host " -> Démarrage de $service..." -ForegroundColor DarkGray
    cd $service
    .\scripts\setup.ps1
    cd ..
}

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host " DÉPLOIEMENT COMPLET TERMINÉ !           " -ForegroundColor Green
Write-Host " Vérifie l'état avec : docker ps         " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan