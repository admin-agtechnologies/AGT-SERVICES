"""AGT Notification Service v1.0 - Services : cache user, preferences, idempotency."""
import logging
import httpx
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


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
            resp = httpx.get(f"{url}/users/by-auth/{user_id}", timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data, timeout=getattr(settings, "USER_CACHE_TTL", 300))
                return data
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
