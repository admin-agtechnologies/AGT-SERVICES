Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " RESET MVP - AG TECHNOLOGIES (DEV)       " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "`n[1/4] Arrêt et suppression des conteneurs..." -ForegroundColor Yellow
$containers = docker ps -aq
if ($containers) {
    docker stop $containers | Out-Null
    docker rm $containers | Out-Null
    Write-Host " -> Conteneurs supprimés." -ForegroundColor Green
}

Write-Host "`n[2/4] Suppression des réseaux (conservation des volumes)..." -ForegroundColor Yellow
$networks = docker network ls -q
if ($networks) {
    # On ignore les erreurs car Docker refusera de supprimer bridge, host et none
    docker network rm $networks 2>$null
    Write-Host " -> Réseaux personnalisés supprimés." -ForegroundColor Green
}

Write-Host "`n[3/4] Suppression des anciens fichiers .env pour forcer la mise à jour..." -ForegroundColor Yellow
Remove-Item -Path "agt-auth\.env" -ErrorAction SilentlyContinue
Remove-Item -Path "agt-users\.env" -ErrorAction SilentlyContinue
Remove-Item -Path "agt-notification\.env" -ErrorAction SilentlyContinue
Write-Host " -> Fichiers .env nettoyés." -ForegroundColor Green

Write-Host "`n[4/4] Lancement du déploiement MVP..." -ForegroundColor Yellow
.\deploy_mvp.ps1