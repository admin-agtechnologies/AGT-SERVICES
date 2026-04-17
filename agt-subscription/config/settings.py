"""AGT Subscription Service v1.0 - Django Settings"""
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1,0.0.0.0").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",          # Requis par DRF (AnonymousUser)
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "django_celery_beat",           # Scheduler Beat (crons CDC)
    "apps.plans",
    "apps.subscriptions",
    "apps.quotas",
    "apps.organizations",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
        ]},
    },
]

# --- Base de données ---
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
    )
}

# --- Cache Redis ---
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/4")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# --- RabbitMQ ---
RABBITMQ_URL = config("RABBITMQ_URL", default="amqp://guest:guest@localhost:5672//")

# --- Celery ---
CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default=f"redis://localhost:6379/5")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# --- Auth JWT (clé publique RSA) ---
AUTH_SERVICE_PUBLIC_KEY_PATH = config(
    "AUTH_SERVICE_PUBLIC_KEY_PATH",
    default=str(BASE_DIR / "keys" / "auth_public.pem"),
)

# --- Services externes ---
USERS_SERVICE_URL = config("USERS_SERVICE_URL", default="http://agt-users-service:7001/api/v1")
PAYMENT_SERVICE_URL = config("PAYMENT_SERVICE_URL", default="http://agt-payment-service:7005/api/v1")
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", default="http://agt-notification-service:7002/api/v1")

# --- S2S Credentials ---
S2S_AUTH_URL = config("S2S_AUTH_URL", default="")
S2S_CLIENT_ID = config("S2S_CLIENT_ID", default="")
S2S_CLIENT_SECRET = config("S2S_CLIENT_SECRET", default="")

# --- Cache TTL ---
QUOTA_CACHE_TTL = config("QUOTA_CACHE_TTL", default=30, cast=int)   # 30s CDC NF-10
USER_STATUS_CACHE_TTL = config("USER_STATUS_CACHE_TTL", default=60, cast=int)  # 60s CDC

# --- REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "common.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# --- Swagger (drf-spectacular) ---
SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Subscription Service",
    "DESCRIPTION": "Plans, abonnements, quotas temps réel, prorata, trial, organisations B2B.",
    "VERSION": "1.0.0",
    "SECURITY": [{"BearerAuth": []}],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
    "COMPONENT_SPLIT_REQUEST": True,
}

# --- CORS ---
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://localhost:3001",
).split(",")

# --- Static ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"