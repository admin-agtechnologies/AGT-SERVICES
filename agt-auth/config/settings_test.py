"""
Settings de test — base SQLite en mémoire, cache local, clés RSA de test.
"""
from config.settings import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

_test_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
JWT_PRIVATE_KEY = _test_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
).decode()
JWT_PUBLIC_KEY = _test_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode()

BCRYPT_ROUNDS = 4
ADMIN_API_KEY = "test-admin-key-for-tests-only"
NOTIFICATION_SERVICE_URL = ""
USERS_SERVICE_URL = ""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {"null": {"class": "logging.NullHandler"}},
    "root": {"handlers": ["null"]},
}
