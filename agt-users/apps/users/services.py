"""
AGT Users Service v1.0 - Services : Cache, Notification, Auth client.
"""
import logging
import uuid
import httpx
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class PermissionCacheService:
    @staticmethod
    def _key(user_id, platform_id, perm_name):
        return f"perm:{user_id}:{platform_id}:{perm_name}"

    @classmethod
    def get(cls, user_id, platform_id, perm_name):
        return cache.get(cls._key(user_id, platform_id, perm_name))

    @classmethod
    def set(cls, user_id, platform_id, perm_name, result):
        cache.set(cls._key(user_id, platform_id, perm_name), result, timeout=getattr(settings, "PERMISSION_CACHE_TTL", 300))

    @classmethod
    def invalidate_user_platform(cls, user_id, platform_id):
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            keys = conn.keys(f"perm:{user_id}:{platform_id}:*")
            if keys:
                conn.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache invalidation failed: {e}")

    @classmethod
    def invalidate_role(cls, role_id):
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            keys = conn.keys("perm:*")
            if keys:
                conn.delete(*keys)
        except Exception as e:
            logger.warning(f"Role cache invalidation failed: {e}")


class ProfileCacheService:
    @staticmethod
    def _key(user_id):
        return f"profile:{user_id}"

    @classmethod
    def get(cls, user_id):
        return cache.get(cls._key(user_id))

    @classmethod
    def set(cls, user_id, data):
        cache.set(cls._key(user_id), data, timeout=getattr(settings, "PROFILE_CACHE_TTL", 60))

    @classmethod
    def invalidate(cls, user_id):
        cache.delete(cls._key(user_id))


class NotificationClient:
    @staticmethod
    def send(notification_type, recipient, template, data):
        url = getattr(settings, "NOTIFICATION_SERVICE_URL", "")
        if not url:
            return False
        try:
            resp = httpx.post(f"{url}/notifications/send", json={
                "type": notification_type, "recipient": recipient,
                "template": template, "data": data,
                "idempotency_key": str(uuid.uuid4()),
            }, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Notification error: {e}")
            return False

    @classmethod
    def notify_role_assigned(cls, user_email, role_name, platform_name):
        cls.send("role_assigned", {"email": user_email}, "users_role_assigned",
                 {"role_name": role_name, "platform_name": platform_name})

    @classmethod
    def notify_document_status(cls, user_email, doc_type, doc_status, comment=None):
        cls.send("document_status_update", {"email": user_email}, "users_document_status",
                 {"doc_type": doc_type, "status": doc_status, "comment": comment})


class AuthServiceClient:
    @staticmethod
    def deactivate_user(auth_user_id):
        url = getattr(settings, "AUTH_SERVICE_URL", "")
        admin_key = getattr(settings, "AUTH_ADMIN_API_KEY", "")
        if not url:
            logger.warning("AUTH_SERVICE_URL non configure")
            return False
        try:
            resp = httpx.post(
                f"{url}/auth/admin/deactivate/{auth_user_id}",
                headers={"X-Admin-API-Key": admin_key},
                timeout=5.0,
            )
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Auth deactivate failed: {e}")
            return False

    @staticmethod
    def purge_user(auth_user_id):
        url = getattr(settings, "AUTH_SERVICE_URL", "")
        admin_key = getattr(settings, "AUTH_ADMIN_API_KEY", "")
        if not url:
            return False
        try:
            resp = httpx.delete(
                f"{url}/auth/admin/purge/{auth_user_id}",
                headers={"X-Admin-API-Key": admin_key},
                timeout=10.0,
            )
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Auth purge failed: {e}")
            return False
