"""
AGT Technologies — Renommage container_name : underscores → tirets
Corrige le problème Django RFC 1034/1035 (underscores invalides dans les hostnames HTTP).

Remplace agt_xxx_yyy → agt-xxx-yyy dans tous les fichiers impactés.
Le réseau agt_network n'est PAS touché (ce n'est pas un hostname HTTP).

Usage : python fix_container_names.py (depuis la racine AGT-SERVICES/)
"""
import os
import re

# =============================================================================
# Mapping des renommages
# =============================================================================

# Format : (ancien, nouveau)
# On ne touche PAS à agt_network (réseau Docker, pas un hostname HTTP)
CONTAINER_RENAMES = [
    # Infra
    ("agt_gateway", "agt-gateway"),
    ("agt_rabbitmq", "agt-rabbitmq"),
    ("agt_mailpit", "agt-mailpit"),
    ("agt_elasticsearch", "agt-elasticsearch"),
    # Auth
    ("agt_auth_service", "agt-auth-service"),
    ("agt_auth_db", "agt-auth-db"),
    ("agt_auth_redis", "agt-auth-redis"),
    ("agt_auth_dev", "agt-auth-dev"),
    # Users
    ("agt_users_service", "agt-users-service"),
    ("agt_users_db", "agt-users-db"),
    ("agt_users_redis", "agt-users-redis"),
    ("agt_users_dev", "agt-users-dev"),
    # Notification
    ("agt_notif_service", "agt-notif-service"),
    ("agt_notif_db", "agt-notif-db"),
    ("agt_notif_redis", "agt-notif-redis"),
    ("agt_notif_worker", "agt-notif-worker"),
    ("agt_notif_beat", "agt-notif-beat"),
    ("agt_notif_dev", "agt-notif-dev"),
    # Subscription
    ("agt_sub_service", "agt-sub-service"),
    ("agt_sub_db", "agt-sub-db"),
    ("agt_sub_redis", "agt-sub-redis"),
    ("agt_sub_dev", "agt-sub-dev"),
    # Payment
    ("agt_pay_service", "agt-pay-service"),
    ("agt_pay_db", "agt-pay-db"),
    ("agt_pay_redis", "agt-pay-redis"),
    ("agt_pay_dev", "agt-pay-dev"),
    # Wallet
    ("agt_wallet_service", "agt-wallet-service"),
    ("agt_wallet_db", "agt-wallet-db"),
    ("agt_wallet_redis", "agt-wallet-redis"),
    ("agt_wallet_dev", "agt-wallet-dev"),
    # Search
    ("agt_search_service", "agt-search-service"),
    ("agt_search_db", "agt-search-db"),
    ("agt_search_redis", "agt-search-redis"),
    ("agt_search_dev", "agt-search-dev"),
    # Chatbot
    ("agt_chatbot_service", "agt-chatbot-service"),
    ("agt_chatbot_db", "agt-chatbot-db"),
    ("agt_chatbot_redis", "agt-chatbot-redis"),
    ("agt_chatbot_dev", "agt-chatbot-dev"),
    # Simulateurs
    ("agt_media_simulator", "agt-media-simulator"),
    ("agt_media_service", "agt-media-service"),
    ("agt_chat_simulator", "agt-chat-simulator"),
    ("agt_chat_service", "agt-chat-service"),
    ("agt_geoloc_simulator", "agt-geoloc-simulator"),
    ("agt_geoloc_service", "agt-geoloc-service"),
]

# Fichiers à traiter
FILES_TO_PROCESS = [
    # Infra
    "docker-compose.infra.yml",
    # Auth
    "agt-auth/docker-compose.yml",
    "agt-auth/.env.example",
    "agt-auth/.env",
    # Users
    "agt-users/docker-compose.yml",
    "agt-users/.env.example",
    "agt-users/.env",
    # Notification
    "agt-notification/docker-compose.yml",
    "agt-notification/.env.example",
    "agt-notification/.env",
    # Subscription
    "agt-subscription/docker-compose.yml",
    "agt-subscription/.env.example",
    "agt-subscription/.env",
    # Payment
    "agt-payment/docker-compose.yml",
    "agt-payment/.env.example",
    "agt-payment/.env",
    # Wallet
    "agt-wallet/docker-compose.yml",
    "agt-wallet/.env.example",
    "agt-wallet/.env",
    # Search
    "agt-search/docker-compose.yml",
    "agt-search/.env.example",
    "agt-search/.env",
    # Chatbot
    "agt-chatbot/docker-compose.yml",
    "agt-chatbot/.env.example",
    "agt-chatbot/.env",
    # Simulateurs
    "agt-media/docker-compose.yml",
    "agt-chat/docker-compose.yml",
    "agt-geoloc/docker-compose.yml",
    # Scripts deploy/reset
    "deploy_mvp.ps1",
    "deploy_mvp.sh",
    "deploy_all.ps1",
    "deploy_all.sh",
    "reset_mvp.ps1",
    "reset_mvp.sh",
    "reset_all.ps1",
    "reset_all.sh",
    # Gateway
    "gateway/nginx.conf",
    # Standards & docs
    "STANDARDS.md",
    "standards.md",
    "README.md",
]


def process_file(filepath):
    """Applique tous les renommages sur un fichier."""
    if not os.path.exists(filepath):
        return None  # Fichier absent, on skip silencieusement

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    for old_name, new_name in CONTAINER_RENAMES:
        if old_name in content:
            count = content.count(old_name)
            content = content.replace(old_name, new_name)
            changes.append(f"    {old_name} → {new_name} ({count}x)")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return []


def main():
    print("=" * 60)
    print("AGT Technologies — Fix container_name (underscores → tirets)")
    print("=" * 60)

    if not os.path.isdir("agt-auth"):
        print("[ERROR] Lancez ce script depuis la racine AGT-SERVICES/")
        return

    total_files = 0
    total_changes = 0

    for filepath in FILES_TO_PROCESS:
        result = process_file(filepath)
        if result is None:
            continue  # Fichier absent
        elif len(result) > 0:
            total_files += 1
            total_changes += len(result)
            print(f"\n  [OK] {filepath}")
            for change in result:
                print(change)
        # Fichier existant mais rien à changer = on ne dit rien

    # Résumé
    print(f"\n{'=' * 60}")
    print(f"  {total_files} fichier(s) modifié(s), {total_changes} remplacement(s)")
    print(f"{'=' * 60}")
    print()
    print("Prochaines étapes :")
    print("  1. docker stop $(docker ps -aq) && docker rm $(docker ps -aq)")
    print("  2. .\\reset_mvp.ps1 --clean")
    print("  3. Relancer les migrations (makemigrations + migrate)")
    print("  4. Recréer la plateforme + templates")
    print("  5. Tester l'inscription")
    print()
    print("IMPORTANT : le réseau agt_network n'a PAS été touché.")
    print("=" * 60)


if __name__ == "__main__":
    main()