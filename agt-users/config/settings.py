"""
AGT Users Service v1.0 - Django Settings
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "apps.users",
    "apps.roles",
    "apps.documents",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
}]

import dj_database_url
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
    )
}

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/1")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

def _read_key(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

AUTH_SERVICE_URL = config("AUTH_SERVICE_URL", default="")
AUTH_ADMIN_API_KEY = config("AUTH_ADMIN_API_KEY", default="")
AUTH_PUBLIC_KEY = _read_key(
    config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem"))
)

MEDIA_SERVICE_URL = config("MEDIA_SERVICE_URL", default="")
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", default="")

PERMISSION_CACHE_TTL = config("PERMISSION_CACHE_TTL", default=300, cast=int)
PROFILE_CACHE_TTL = config("PROFILE_CACHE_TTL", default=60, cast=int)
DEFAULT_HARD_DELETE_DELAY_DAYS = config("DEFAULT_HARD_DELETE_DELAY_DAYS", default=30, cast=int)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["apps.users.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.users.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.users.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Users Service API",
    "DESCRIPTION": "Service de gestion des utilisateurs : profils, RBAC dynamique, documents, metadonnees.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {"name": "Health", "description": "Etat du service"},
        {"name": "Profile", "description": "CRUD profil utilisateur"},
        {"name": "Sync", "description": "Synchronisation depuis Auth"},
        {"name": "Addresses", "description": "CRUD adresses"},
        {"name": "Roles", "description": "CRUD roles par plateforme"},
        {"name": "Permissions", "description": "CRUD permissions et verification"},
        {"name": "User Roles", "description": "Assignation roles aux utilisateurs"},
        {"name": "Documents", "description": "Documents KYC et workflow validation"},
        {"name": "Metadata", "description": "Metadonnees cle-valeur par plateforme"},
    ],
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    "SECURITY": [{"BearerAuth": []}],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": False,
    },
}

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
