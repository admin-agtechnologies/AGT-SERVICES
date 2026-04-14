"""AGT Notification Service v1.0 - Services : cache user, preferences, idempotency."""
import logging
import httpx
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class S2STokenService:
    """
    Gère l'obtention et le renouvellement du token S2S de Notification.
    Le token est mis en cache Redis avec une marge de sécurité avant expiration.
    """
    CACHE_KEY = "notif_s2s_token"
    MARGIN_SECONDS = 60  # renouveler 60s avant expiration

    @staticmethod
    def get_token() -> str:
        # 1. Vérifier le cache Redis
        cached = cache.get(S2STokenService.CACHE_KEY)
        if cached:
            return cached

        # 2. Appeler Auth pour obtenir un nouveau token
        auth_url = getattr(settings, "S2S_AUTH_URL", "")
        client_id = getattr(settings, "S2S_CLIENT_ID", "")
        client_secret = getattr(settings, "S2S_CLIENT_SECRET", "")

        if not all([auth_url, client_id, client_secret]):
            logger.error("S2S credentials manquants dans la config Notification.")
            return ""

        try:
            resp = httpx.post(f"{auth_url}/auth/s2s/token", json={
                "client_id": client_id,
                "client_secret": client_secret,
            }, timeout=5.0)

            if resp.status_code != 200:
                logger.error(f"S2S token refresh échoué ({resp.status_code}): {resp.text}")
                return ""

            data = resp.json()
            token = data.get("access_token", "")
            expires_in = data.get("expires_in", 3600)

            # Mettre en cache avec marge de sécurité
            ttl = max(expires_in - S2STokenService.MARGIN_SECONDS, 60)
            cache.set(S2STokenService.CACHE_KEY, token, timeout=ttl)

            return token

        except Exception as e:
            logger.error(f"S2S token refresh exception: {e}")
            return ""
class UserResolverService:
    @staticmethod
    def get_user(user_id):
        cache_key = f"user_coords:{user_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return None

        try:
            token = S2STokenService.get_token()
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            resp = httpx.get(f"{url}/users/by-auth/{user_id}", headers=headers, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data, timeout=getattr(settings, "USER_CACHE_TTL", 300))
                return data
            logger.warning(f"UserResolver: {resp.status_code} pour user {user_id}")
        except Exception as e:
            logger.error(f"User resolve failed: {e}")
        return None

class PreferenceService:
    @staticmethod
    def is_allowed(user_id, platform_id, channel, category):
        if category == "security":
            return True
        from apps.notifications.models import UserPreference
        try:
            pref = UserPreference.objects.get(user_id=user_id, platform_id=platform_id)
        except UserPreference.DoesNotExist:
            return category != "marketing"
        return pref.is_channel_enabled(channel) and pref.is_category_enabled(category)


class IdempotencyService:
    @staticmethod
    def check_and_register(platform_id, key):
        cache_key = f"idemp:{platform_id}:{key}"
        if cache.get(cache_key):
            return True
        cache.set(cache_key, True, timeout=getattr(settings, "IDEMPOTENCY_TTL", 86400))
        return False
