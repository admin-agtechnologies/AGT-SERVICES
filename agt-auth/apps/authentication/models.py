"""
AGT Auth Service v1.0 — Modèles Django
Conforme au MLD du CDC Auth.
Tables : platforms, users_auth, sessions, refresh_tokens, oauth_providers, login_history, verification_tokens
"""
import uuid
import bcrypt

from django.db import models
from django.utils import timezone


class Platform(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    allowed_auth_methods = models.JSONField(default=list)
    allowed_redirect_urls = models.JSONField(default=list)
    client_secret_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platforms"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    def verify_client_secret(self, raw_secret: str) -> bool:
        return bcrypt.checkpw(raw_secret.encode("utf-8"), self.client_secret_hash.encode("utf-8"))

    @staticmethod
    def hash_client_secret(raw_secret: str, rounds: int = 12) -> str:
        return bcrypt.hashpw(raw_secret.encode("utf-8"), bcrypt.gensalt(rounds=rounds)).decode("utf-8")


class AuthMethodChoice(models.TextChoices):
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"
    GOOGLE = "google", "Google"
    FACEBOOK = "facebook", "Facebook"


class UserAuth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    two_fa_enabled = models.BooleanField(default=False)
    two_fa_secret = models.CharField(max_length=255, null=True, blank=True)
    registration_method = models.CharField(max_length=20, choices=AuthMethodChoice.choices)
    registration_platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="registered_users")
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_auth"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return self.email or self.phone or str(self.id)

    def set_password(self, raw_password: str) -> None:
        from django.conf import settings
        rounds = getattr(settings, "BCRYPT_ROUNDS", 12)
        self.password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt(rounds=rounds)).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        if not self.password_hash:
            return False
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def is_locked(self) -> bool:
        if self.locked_until and self.locked_until > timezone.now():
            return True
        if self.locked_until and self.locked_until <= timezone.now():
            self.failed_login_attempts = 0
            self.locked_until = None
            self.save(update_fields=["failed_login_attempts", "locked_until"])
        return False

    def increment_failed_attempts(self) -> None:
        from django.conf import settings
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= getattr(settings, "BRUTE_FORCE_MAX", 5):
            lockout = getattr(settings, "BRUTE_FORCE_LOCKOUT", 900)
            self.locked_until = timezone.now() + timezone.timedelta(seconds=lockout)
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def reset_failed_attempts(self) -> None:
        if self.failed_login_attempts > 0:
            self.failed_login_attempts = 0
            self.locked_until = None
            self.save(update_fields=["failed_login_attempts", "locked_until"])

    @property
    def is_available_for_login(self):
        if self.is_blocked:
            return False, "user_blocked"
        if self.is_deactivated:
            return False, "user_deactivated"
        if self.is_locked():
            return False, "account_locked"
        return True, ""


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="sessions")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="sessions")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "sessions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["expires_at"]),
        ]

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()

    def revoke(self) -> None:
        self.is_active = False
        self.save(update_fields=["is_active"])


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="refresh_tokens")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="refresh_tokens")
    token_hash = models.CharField(max_length=255, unique=True)
    is_revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "refresh_tokens"
        ordering = ["created_at"]
        indexes = [models.Index(fields=["user", "is_revoked"])]

    def revoke(self) -> None:
        self.is_revoked = True
        self.save(update_fields=["is_revoked"])

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()


class OAuthProvider(models.Model):
    PROVIDER_CHOICES = [("google", "Google"), ("facebook", "Facebook")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="oauth_providers")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_user_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "oauth_providers"
        constraints = [
            models.UniqueConstraint(fields=["user", "provider"], name="unique_user_provider"),
            models.UniqueConstraint(fields=["provider", "provider_user_id"], name="unique_provider_user_id"),
        ]


class LoginHistory(models.Model):
    LOGIN_METHOD_CHOICES = [
        ("email", "Email/Password"), ("phone", "Phone/OTP"),
        ("google", "Google OAuth"), ("facebook", "Facebook OAuth"),
        ("magic_link", "Magic Link"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="login_history")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="login_history")
    method = models.CharField(max_length=20, choices=LOGIN_METHOD_CHOICES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    success = models.BooleanField()
    failure_reason = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "login_history"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["platform", "created_at"]),
        ]


class VerificationToken(models.Model):
    TOKEN_TYPE_CHOICES = [
        ("email_verification", "Email Verification"),
        ("password_reset", "Password Reset"),
        ("magic_link", "Magic Link"),
        ("phone_otp", "Phone OTP"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="verification_tokens")
    token_hash = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=30, choices=TOKEN_TYPE_CHOICES)
    payload = models.JSONField(null=True, blank=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "verification_tokens"
        indexes = [models.Index(fields=["type", "expires_at"])]

    @property
    def is_valid(self) -> bool:
        return self.used_at is None and self.expires_at > timezone.now()

    def mark_as_used(self) -> None:
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])
