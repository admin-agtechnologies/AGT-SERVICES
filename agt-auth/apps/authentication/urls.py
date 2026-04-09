"""
AGT Auth Service v1.0 — URLs
"""
from django.urls import path
from apps.authentication.views_auth import (
    HealthCheckView, RegisterView, VerifyEmailView, VerifyOTPView,
    LoginView, LoginPhoneView, MagicLinkRequestView, MagicLinkCallbackView,
)
from apps.authentication.views_sessions import (
    RefreshTokenView, LogoutView, SessionListView, SessionRevokeView,
    VerifyTokenView, TokenExchangeView, ForgotPasswordView, ResetPasswordView,
    ChangePasswordView, TwoFAEnableView, TwoFAConfirmView, TwoFAVerifyView,
    TwoFADisableView, MeView, LoginHistoryView, UserStatsView,
)
from apps.authentication.views_admin import (
    AdminBlockUserView, AdminUnblockUserView, AccountDeactivateView,
    AdminDeactivateUserView, AdminPurgeUserView,
    OAuthGoogleInitView, OAuthGoogleCallbackView,
    OAuthFacebookInitView, OAuthFacebookCallbackView,
    S2STokenView, S2SIntrospectView,
)

urlpatterns = [
    # Health
    path("auth/health", HealthCheckView.as_view(), name="auth-health"),

    # Register & Verify
    path("auth/register", RegisterView.as_view(), name="auth-register"),
    path("auth/verify-email", VerifyEmailView.as_view(), name="auth-verify-email"),
    path("auth/verify-otp", VerifyOTPView.as_view(), name="auth-verify-otp"),

    # Login
    path("auth/login", LoginView.as_view(), name="auth-login"),
    path("auth/login/phone", LoginPhoneView.as_view(), name="auth-login-phone"),
    path("auth/login/magic-link", MagicLinkRequestView.as_view(), name="auth-magic-link"),
    path("auth/magic-link/callback", MagicLinkCallbackView.as_view(), name="auth-magic-link-callback"),

    # OAuth
    path("auth/oauth/google", OAuthGoogleInitView.as_view(), name="auth-oauth-google"),
    path("auth/oauth/google/callback", OAuthGoogleCallbackView.as_view(), name="auth-oauth-google-callback"),
    path("auth/oauth/facebook", OAuthFacebookInitView.as_view(), name="auth-oauth-facebook"),
    path("auth/oauth/facebook/callback", OAuthFacebookCallbackView.as_view(), name="auth-oauth-facebook-callback"),

    # Password
    path("auth/forgot-password", ForgotPasswordView.as_view(), name="auth-forgot-password"),
    path("auth/reset-password", ResetPasswordView.as_view(), name="auth-reset-password"),
    path("auth/change-password", ChangePasswordView.as_view(), name="auth-change-password"),

    # 2FA
    path("auth/2fa/enable", TwoFAEnableView.as_view(), name="auth-2fa-enable"),
    path("auth/2fa/confirm", TwoFAConfirmView.as_view(), name="auth-2fa-confirm"),
    path("auth/2fa/verify", TwoFAVerifyView.as_view(), name="auth-2fa-verify"),
    path("auth/2fa/disable", TwoFADisableView.as_view(), name="auth-2fa-disable"),

    # Sessions & Tokens
    path("auth/refresh", RefreshTokenView.as_view(), name="auth-refresh"),
    path("auth/logout", LogoutView.as_view(), name="auth-logout"),
    path("auth/sessions", SessionListView.as_view(), name="auth-sessions"),
    path("auth/sessions/<uuid:session_id>", SessionRevokeView.as_view(), name="auth-session-revoke"),
    path("auth/verify-token", VerifyTokenView.as_view(), name="auth-verify-token"),
    path("auth/token/exchange", TokenExchangeView.as_view(), name="auth-token-exchange"),

    # Profile & Audit
    path("auth/me", MeView.as_view(), name="auth-me"),
    path("auth/login-history", LoginHistoryView.as_view(), name="auth-login-history"),
    path("auth/stats/<uuid:user_id>", UserStatsView.as_view(), name="auth-stats"),

    # Administration
    path("auth/admin/block/<uuid:user_id>", AdminBlockUserView.as_view(), name="auth-admin-block"),
    path("auth/admin/unblock/<uuid:user_id>", AdminUnblockUserView.as_view(), name="auth-admin-unblock"),
    path("auth/account/deactivate", AccountDeactivateView.as_view(), name="auth-account-deactivate"),
    path("auth/admin/deactivate/<uuid:auth_user_id>", AdminDeactivateUserView.as_view(), name="auth-admin-deactivate"),
    path("auth/admin/purge/<uuid:auth_user_id>", AdminPurgeUserView.as_view(), name="auth-admin-purge"),

    # S2S
    path("auth/s2s/token", S2STokenView.as_view(), name="auth-s2s-token"),
    path("auth/s2s/introspect", S2SIntrospectView.as_view(), name="auth-s2s-introspect"),
]
