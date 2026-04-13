#!/bin/bash

# deploy_all.sh
echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m DÉPLOIEMENT COMPLET - AG TECHNOLOGIES   \e[0m"
echo -e "\e[36m=========================================\e[0m"

# 1. Infra partagée
echo -e "\n\e[33m[1/5] Lancement de l'infrastructure partagée...\e[0m"
docker compose -f "Docker compose.infra.yml" up -d

# 2. Simulateurs
echo -e "\n\e[33m[2/5] Lancement des simulateurs (Media, Chat, Geoloc)...\e[0m"
for sim in agt-media agt-chat agt-geoloc; do
    echo -e "\e[90m -> Démarrage de $sim...\e[0m"
    cd $sim && docker compose up -d --build && cd ..
done

# 3. Auth
echo -e "\n\e[33m[3/5] Lancement du Service Auth...\e[0m"
cd agt-auth && bash scripts/setup.sh && cd ..

echo -e "\e[90mAttente de la génération des clés...\e[0m"
sleep 5

# 4. Partage des clés
echo -e "\n\e[33m[4/5] Partage de la clé publique Auth...\e[0m"
AUTH_PUB_KEY="agt-auth/keys/public.pem"
TARGET_SERVICES=("agt-users" "agt-notification" "agt-subscription" "agt-payment" "agt-wallet" "agt-search" "agt-chatbot")

if [ -f "$AUTH_PUB_KEY" ]; then
    for service in "${TARGET_SERVICES[@]}"; do
        mkdir -p "$service/keys"
        cp "$AUTH_PUB_KEY" "$service/keys/auth_public.pem"
        echo -e "\e[90m -> Clé copiée vers $service\e[0m"
    done
    echo -e "\e[32mToutes les clés ont été distribuées.\e[0m"
else
    echo -e "\e[31mATTENTION: Clé publique Auth introuvable !\e[0m"
fi

# 5. Autres services
echo -e "\n\e[33m[5/5] Lancement des services métier restants...\e[0m"
for service in "${TARGET_SERVICES[@]}"; do
    echo -e "\e[90m -> Démarrage de $service...\e[0m"
    cd $service && bash scripts/setup.sh && cd ..
done

echo -e "\n\e[36m=========================================\e[0m"
echo -e "\e[32m DÉPLOIEMENT COMPLET TERMINÉ !           \e[0m"
echo -e "\e[36m Vérifie l'état avec : docker ps         \e[0m"
echo -e "\e[36m=========================================\e[0m"