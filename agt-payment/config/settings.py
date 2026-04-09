from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.staticfiles", "rest_framework", "drf_spectacular", "corsheaders", "apps.payments", "apps.providers", "apps.webhooks"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]
import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/5")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL, "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
def _read_key(path):
    try:
        with open(path, "r") as f: return f.read()
    except FileNotFoundError: return ""
AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ["common.authentication.JWTAuthentication"], "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"], "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"], "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", "UNAUTHENTICATED_USER": None}
SPECTACULAR_SETTINGS = {"TITLE": "AGT Payment Service API", "VERSION": "1.0.0", "DESCRIPTION": "Paiements multi-provider: Orange Money, MTN MoMo, Stripe, PayPal.", "TAGS": [{"name": "Health"}, {"name": "Payments"}, {"name": "Webhooks"}, {"name": "Providers"}, {"name": "Admin"}]}
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {"version": 1, "disable_existing_loggers": False, "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}
