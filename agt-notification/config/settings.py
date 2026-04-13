"""AGT Notification Service v1.0 - Django Settings"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes", "django.contrib.staticfiles",
    "django_celery_beat", "rest_framework", "drf_spectacular", "corsheaders",
    "apps.notifications", "apps.templates_mgr", "apps.campaigns", "apps.devices",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
              "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]

import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/2")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL,
                       "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}

CELERY_BROKER_URL = config("RABBITMQ_URL", default=config("CELERY_BROKER_URL", default="amqp://guest:guest@localhost:5672//"))
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/3")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_ACKS_LATE = True

def _read_key(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
AUTH_SERVICE_URL = config("AUTH_SERVICE_URL", default="")
USERS_SERVICE_URL = config("USERS_SERVICE_URL", default="")
USER_CACHE_TTL = config("USER_CACHE_TTL", default=300, cast=int)
IDEMPOTENCY_TTL = config("IDEMPOTENCY_TTL", default=86400, cast=int)

SENDGRID_API_KEY = config("SENDGRID_API_KEY", default="")
MAILGUN_API_KEY = config("MAILGUN_API_KEY", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@agtechnologies.com")
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default="")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default="")
TWILIO_FROM_NUMBER = config("TWILIO_FROM_NUMBER", default="")
FCM_SERVER_KEY = config("FCM_SERVER_KEY", default="")
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='mailpit')
EMAIL_PORT = config('EMAIL_PORT', default=1025, cast=int)
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["apps.notifications.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.notifications.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.notifications.pagination.StandardPagination",
    "PAGE_SIZE": 20, "UNAUTHENTICATED_USER": None,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Notification Service API", "VERSION": "1.0.0",
    "DESCRIPTION": "Envoi multi-canal, templates dynamiques, campagnes, preferences, in-app.",
    "TAGS": [
        {"name": "Health"}, {"name": "Send", "description": "Envoi notifications"},
        {"name": "Templates"}, {"name": "Campaigns"}, {"name": "Preferences"},
        {"name": "In-App"}, {"name": "Devices"}, {"name": "Stats"}, {"name": "Config"},
    ],
}

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {"version": 1, "disable_existing_loggers": False,
           "handlers": {"console": {"class": "logging.StreamHandler"}},
           "root": {"handlers": ["console"], "level": "INFO"}}
