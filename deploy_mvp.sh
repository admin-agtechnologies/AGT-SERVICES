#!/bin/bash

# deploy_mvp.sh
echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m DÉPLOIEMENT MVP - AG TECHNOLOGIES (PROD)\e[0m"
echo -e "\e[36m=========================================\e[0m"

# 1. Lancement de l'infrastructure partagée
echo -e "\n\e[33m[1/5] Lancement de l'infrastructure partagée...\e[0m"
docker compose -f "Docker compose.infra.yml" up -d

# 2. Lancement du simulateur Média
echo -e "\n\e[33m[2/5] Lancement du simulateur Média...\e[0m"
cd agt-media && docker compose up -d --build && cd ..

# 3. Lancement de Auth
echo -e "\n\e[33m[3/5] Lancement du Service Auth...\e[0m"
cd agt-auth && bash scripts/setup.sh && cd ..

# Attendre la génération des clés
sleep 5

# 4. Partage de la clé publique
echo -e "\n\e[33m[4/5] Partage de la clé publique Auth...\e[0m"
AUTH_PUB_KEY="agt-auth/keys/public.pem"
if [ -f "$AUTH_PUB_KEY" ]; then
    mkdir -p agt-users/keys agt-notification/keys
    cp "$AUTH_PUB_KEY" agt-users/keys/auth_public.pem
    cp "$AUTH_PUB_KEY" agt-notification/keys/auth_public.pem
    echo -e "\e[32mClés copiées avec succès.\e[0m"
else
    echo -e "\e[31mATTENTION: Clé publique Auth introuvable !\e[0m"
fi

# 5. Lancement de Users et Notification
echo -e "\n\e[33m[5/5] Lancement des Services Users et Notification...\e[0m"
cd agt-users && bash scripts/setup.sh && cd ..
cd agt-notification && bash scripts/setup.sh && cd ..

echo -e "\n\e[36m=========================================\e[0m"
echo -e "\e[32m DÉPLOIEMENT MVP TERMINÉ !               \e[0m"
echo -e "\e[36m Vérifie l'état avec : docker ps         \e[0m"
echo -e "\e[36m=========================================\e[0m"