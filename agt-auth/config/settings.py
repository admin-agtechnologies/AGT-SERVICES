"""
AGT Auth Service v1.0 — Django Settings
"""
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Sécurité ─────────────────────────────────────────────────────────────────
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

# ─── Applications ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "apps.authentication",
    "apps.platforms",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.RateLimitMiddleware",
    "common.middleware.CSRFCookieProtectionMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ─── Base de données ──────────────────────────────────────────────────────────
import dj_database_url  # noqa: E402

DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
        ssl_require=False,
    )
}

# ─── Cache (Redis) ────────────────────────────────────────────────────────────
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
    }
}

# ─── JWT ──────────────────────────────────────────────────────────────────────
def _read_key(path_env_var: str, default_path: str) -> str:
    path = config(path_env_var, default=default_path)
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


JWT_PRIVATE_KEY = _read_key("JWT_PRIVATE_KEY_PATH", str(BASE_DIR / "keys/private.pem"))
JWT_PUBLIC_KEY = _read_key("JWT_PUBLIC_KEY_PATH", str(BASE_DIR / "keys/public.pem"))
JWT_ACCESS_TTL = config("JWT_ACCESS_TTL", default=900, cast=int)
JWT_REFRESH_TTL = config("JWT_REFRESH_TTL", default=604800, cast=int)
JWT_ISSUER = config("JWT_ISSUER", default="agt-auth")
JWT_AUDIENCE = config("JWT_AUDIENCE", default="agt-ecosystem")

# ─── Sécurité Auth ────────────────────────────────────────────────────────────
BCRYPT_ROUNDS = config("BCRYPT_ROUNDS", default=12, cast=int)
ADMIN_API_KEY = config("ADMIN_API_KEY", default="")
MAX_REFRESH_TOKENS = config("MAX_REFRESH_TOKENS", default=5, cast=int)

# ─── Tokens durées de vie ─────────────────────────────────────────────────────
OTP_TTL = config("OTP_TTL", default=300, cast=int)
MAGIC_LINK_TTL = config("MAGIC_LINK_TTL", default=600, cast=int)

# ─── Rate Limiting ────────────────────────────────────────────────────────────
RATE_LIMIT_LOGIN = config("RATE_LIMIT_LOGIN", default=10, cast=int)
BRUTE_FORCE_MAX = config("BRUTE_FORCE_MAX", default=5, cast=int)
BRUTE_FORCE_LOCKOUT = config("BRUTE_FORCE_LOCKOUT", default=900, cast=int)

# ─── Services Inter-microservices ─────────────────────────────────────────────
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", default="")
USERS_SERVICE_URL = config("USERS_SERVICE_URL", default="")

# ─── OAuth ────────────────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET", default="")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI", default="")

FACEBOOK_APP_ID = config("FACEBOOK_APP_ID", default="")
FACEBOOK_APP_SECRET = config("FACEBOOK_APP_SECRET", default="")
FACEBOOK_REDIRECT_URI = config("FACEBOOK_REDIRECT_URI", default="")

# ─── Cookies ──────────────────────────────────────────────────────────────────
COOKIE_SECURE = config("COOKIE_SECURE", default=False, cast=bool)
COOKIE_SAMESITE = config("COOKIE_SAMESITE", default="Lax")

# ─── DRF ──────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.authentication.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.authentication.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.authentication.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

# ─── Swagger / OpenAPI (drf-spectacular) ──────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Auth Service API",
    "DESCRIPTION": "Service d'authentification centralise de l'ecosysteme AG Technologies.\n\nJWT RS256, OAuth Google/Facebook, 2FA TOTP, sessions, S2S tokens.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {"name": "AGT Engineering", "email": "engineering@agt.com"},
    "LICENSE": {"name": "Proprietary"},
    "TAGS": [
        {"name": "Health", "description": "Etat du service"},
        {"name": "Register", "description": "Inscription et verification"},
        {"name": "Login", "description": "Connexion (email, phone, magic link)"},
        {"name": "OAuth", "description": "Authentification sociale (Google, Facebook)"},
        {"name": "Password", "description": "Oubli, reset, changement de mot de passe"},
        {"name": "2FA", "description": "Authentification a double facteur (TOTP)"},
        {"name": "Sessions", "description": "Gestion sessions et tokens"},
        {"name": "Profile", "description": "Profil identite et audit"},
        {"name": "Admin", "description": "Administration (block, deactivate, purge)"},
        {"name": "Platforms", "description": "CRUD plateformes (admin)"},
        {"name": "S2S", "description": "Tokens inter-services (machine-to-machine)"},
    ],
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
    },
}

# ─── CORS ─────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

# ─── Logging ──────────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "apps": {"level": "DEBUG" if DEBUG else "INFO"},
    },
}

# ─── Static files ─────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
