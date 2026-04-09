"""
AGT Auth Service v1.0 — Middleware : Rate limiting Redis + CSRF cookie protection.
"""
import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """Rate limiting par endpoint + global par IP via Redis incr/expire."""

    RATE_LIMITS = {
        "/api/v1/auth/login": {"window": 60, "max": 10},
        "/api/v1/auth/login/phone": {"window": 60, "max": 3},
        "/api/v1/auth/verify-otp": {"window": 60, "max": 5},
        "/api/v1/auth/forgot-password": {"window": 900, "max": 3},
        "/api/v1/auth/register": {"window": 3600, "max": 5},
        "/api/v1/auth/2fa/verify": {"window": 60, "max": 5},
    }

    GLOBAL_WINDOW = 60
    GLOBAL_MAX = 100

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self._get_ip(request)
        path = request.path.rstrip("/")

        # Endpoint-specific
        rule = self.RATE_LIMITS.get(path)
        if rule and request.method == "POST":
            key = f"rl:{path}:{ip}"
            if self._is_limited(key, rule["window"], rule["max"]):
                return JsonResponse(
                    {"success": False, "error": {"code": "RATE_LIMITED", "message": "Trop de requêtes."}},
                    status=429,
                )

        # Global
        if self._is_limited(f"rl:global:{ip}", self.GLOBAL_WINDOW, self.GLOBAL_MAX):
            return JsonResponse(
                {"success": False, "error": {"code": "RATE_LIMITED", "message": "Trop de requêtes."}},
                status=429,
            )

        return self.get_response(request)

    def _is_limited(self, key, window, max_requests):
        try:
            current = cache.get(key, 0)
            if current >= max_requests:
                return True
            # Incrémente atomiquement avec TTL
            if current == 0:
                cache.set(key, 1, timeout=window)
            else:
                cache.incr(key)
            return False
        except Exception:
            return False  # Fail-open

    @staticmethod
    def _get_ip(request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", "0.0.0.0")


class CSRFCookieProtectionMiddleware:
    """Protection CSRF sur endpoints cookie-based (CDC v1.3.2)."""

    PROTECTED_PATHS = {
        "/api/v1/auth/refresh",
        "/api/v1/auth/logout",
        "/api/v1/auth/token/exchange",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip("/")

        if request.method == "POST" and path in self.PROTECTED_PATHS:
            if not getattr(settings, "DEBUG", False):
                xrw = request.headers.get("X-Requested-With", "")
                origin = request.headers.get("Origin", "")
                allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
                if isinstance(allowed, str):
                    allowed = [a.strip() for a in allowed.split(",")]

                if xrw != "XMLHttpRequest" and origin and origin not in allowed:
                    return JsonResponse(
                        {"success": False, "error": {"code": "CSRF_FAILED", "message": "Requête non autorisée."}},
                        status=403,
                    )

        return self.get_response(request)
