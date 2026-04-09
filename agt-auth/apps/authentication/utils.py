"""
AGT Auth Service v1.0 — Utilitaires : extraction IP, gestion cookies sécurisés.
"""
from django.conf import settings


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def set_refresh_cookie(response, raw_refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token", value=raw_refresh_token,
        max_age=settings.JWT_REFRESH_TTL, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/api/v1/auth/refresh",
    )


def set_access_cookie(response, access_token: str) -> None:
    response.set_cookie(
        key="access_token", value=access_token,
        max_age=settings.JWT_ACCESS_TTL, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/",
    )


def clear_refresh_cookie(response) -> None:
    response.set_cookie(
        key="refresh_token", value="", max_age=0, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/api/v1/auth/refresh",
    )


def clear_access_cookie(response) -> None:
    response.set_cookie(
        key="access_token", value="", max_age=0, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/",
    )
