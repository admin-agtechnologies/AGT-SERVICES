"""Settings test - SQLite memoire, cache local, cle RSA generee."""
from config.settings import *  # noqa
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

AUTH_SERVICE_URL = ""
AUTH_ADMIN_API_KEY = "test-admin-key"
NOTIFICATION_SERVICE_URL = ""
MEDIA_SERVICE_URL = ""

LOGGING = {"version": 1, "disable_existing_loggers": True,
           "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}
