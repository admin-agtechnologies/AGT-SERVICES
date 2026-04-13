# deploy_mvp.ps1
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " DÉPLOIEMENT MVP - AG TECHNOLOGIES (DEV) " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 0. Nettoyage du réseau pour éviter les conflits de labels
Write-Host "`n[0/5] Nettoyage du réseau agt_network..." -ForegroundColor DarkGray
if (docker network ls --filter name=^agt_network$ --format="{{.Name}}") {
    docker network rm agt_network | Out-Null
    Write-Host " -> Réseau existant supprimé." -ForegroundColor DarkGray
}

# 1. Lancement de l'infrastructure partagée
Write-Host "`n[1/5] Lancement de l'infrastructure partagée (Gateway, RabbitMQ, Mailpit, ES)..." -ForegroundColor Yellow
docker compose -f "Docker compose.infra.yml" up -d

# 2. Lancement du simulateur Média
Write-Host "`n[2/5] Lancement du simulateur Média..." -ForegroundColor Yellow
cd agt-media
docker compose up -d --build
cd ..

# 3. Lancement de Auth
Write-Host "`n[3/5] Lancement du Service Auth (Génération des clés RSA)..." -ForegroundColor Yellow
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
cd ..

# Attendre un peu que les clés soient générées
Start-Sleep -Seconds 5

# 4. Partage de la clé publique
Write-Host "`n[4/5] Partage de la clé publique Auth vers Users et Notification..." -ForegroundColor Yellow
$authPubKey = "agt-auth\keys\public.pem"
if (Test-Path $authPubKey) {
    New-Item -ItemType Directory -Force -Path "agt-users\keys" | Out-Null
    Copy-Item -Path $authPubKey -Destination "agt-users\keys\auth_public.pem" -Force
    
    New-Item -ItemType Directory -Force -Path "agt-notification\keys" | Out-Null
    Copy-Item -Path $authPubKey -Destination "agt-notification\keys\auth_public.pem" -Force
    Write-Host " -> Clés copiées avec succès." -ForegroundColor Green
} else {
    Write-Host " -> ATTENTION: Clé publique Auth introuvable !" -ForegroundColor Red
}

# 5. Lancement de Users et Notification
Write-Host "`n[5/5] Lancement des Services Users et Notification..." -ForegroundColor Yellow
cd agt-users
.\scripts\setup.ps1
cd ..

cd agt-notification
.\scripts\setup.ps1
cd ..

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host " DÉPLOIEMENT MVP TERMINÉ !               " -ForegroundColor Green
Write-Host " Vérifie l'état avec : docker ps         " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan