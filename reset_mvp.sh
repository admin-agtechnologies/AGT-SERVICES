#!/bin/bash
echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m RESET MVP - AG TECHNOLOGIES (DEV)       \e[0m"
echo -e "\e[36m=========================================\e[0m"

echo -e "\n\e[33m[1/4] Arrêt et suppression des conteneurs...\e[0m"
containers=$(docker ps -aq)
if [ -n "$containers" ]; then
    docker stop $containers > /dev/null
    docker rm $containers > /dev/null
    echo -e "\e[32m -> Conteneurs supprimés.\e[0m"
fi

echo -e "\n\e[33m[2/4] Suppression des réseaux (conservation des volumes)...\e[0m"
networks=$(docker network ls -q)
if [ -n "$networks" ]; then
    docker network rm $networks 2>/dev/null
    echo -e "\e[32m -> Réseaux personnalisés supprimés.\e[0m"
fi

echo -e "\n\e[33m[3/4] Suppression des anciens fichiers .env pour forcer la mise à jour...\e[0m"
rm -f agt-auth/.env agt-users/.env agt-notification/.env
echo -e "\e[32m -> Fichiers .env nettoyés.\e[0m"

echo -e "\n\e[33m[4/4] Lancement du déploiement MVP...\e