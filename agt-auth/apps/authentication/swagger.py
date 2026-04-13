"""
AGT Auth Service v1.0 - Annotations Swagger/OpenAPI (drf-spectacular).
Importer et appliquer via @extend_schema sur chaque view.
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# --- NOUVEAUX IMPORTS ---
from apps.authentication.serializers import (
    RegisterSerializer, VerifyEmailSerializer, VerifyOTPSerializer,
    LoginSerializer, LoginPhoneSerializer, MagicLinkSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer, ChangePasswordSerializer,
    DeactivateAccountSerializer, TwoFAConfirmSerializer, TwoFAVerifySerializer,
    TwoFADisableSerializer, SessionResponseSerializer, LoginHistoryResponseSerializer,
    UserAuthResponseSerializer
)
from apps.platforms.serializers import PlatformCreateSerializer, PlatformUpdateSerializer, PlatformResponseSerializer
# ------------------------

# --- Health ---
health_schema = extend_schema(
    tags=["Health"],
    summary="Health check",
    description="Verifie l'etat du service (DB, Redis). Aucune authentification requise.",
    responses={
        200: {"type": "object", "properties": {
            "status": {"type": "string", "example": "healthy"},
            "database": {"type": "string", "example": "ok"},
            "redis": {"type": "string", "example": "ok"},
            "version": {"type": "string", "example": "1.0.0"},
        }},
        503: {"description": "Service degraded"},
    },
)

# --- Register ---
register_schema = extend_schema(
    tags=["Register"],
    summary="Inscription (email ou telephone)",
    description="Cree un nouveau compte. Header X-Platform-Id obligatoire. Le flux OAuth ne passe pas par cet endpoint.",
    parameters=[OpenApiParameter(name="X-Platform-Id", location=OpenApiParameter.HEADER, required=True, type=str, description="UUID de la plateforme")],
    request=RegisterSerializer, # <-- CORRECTION ICI
    responses={201: {"description": "Compte cree"}, 400: {"description": "Validation error"}, 409: {"description": "Email/phone deja utilise"}},
)

# --- Login ---
login_schema = extend_schema(
    tags=["Login"],
    summary="Connexion email + mot de passe",
    description="Retourne un access_token JWT. Le refresh_token est pose en cookie HttpOnly.",
    request=LoginSerializer, # <-- CORRECTION ICI
    responses={200: {"description": "Connexion reussie"}, 401: {"description": "Identifiants invalides"}, 403: {"description": "Compte bloque/desactive"}, 429: {"description": "Rate limited"}},
)

login_phone_schema = extend_schema(
    tags=["Login"],
    summary="Demande OTP par SMS",
    description="Envoie un code OTP au numero. Le client soumet ensuite via POST /auth/verify-otp.",
    request=LoginPhoneSerializer, # <-- CORRECTION ICI
)

magic_link_schema = extend_schema(
    tags=["Login"],
    summary="Envoi magic link par email",
    description="Envoie un lien de connexion. Le clic redirige vers le callback qui pose les cookies.",
    request=MagicLinkSerializer, # <-- CORRECTION ICI
)

magic_link_callback_schema = extend_schema(
    tags=["Login"],
    summary="Callback magic link",
    description="Traite le clic sur le magic link. Pose les tokens en cookies HttpOnly et redirige.",
    parameters=[OpenApiParameter(name="token", location=OpenApiParameter.QUERY, required=True, type=str)],
    responses={302: {"description": "Redirect avec cookies"}, 400: {"description": "Token invalide"}, 403: {"description": "Utilisateur bloque"}},
)

# --- Verify ---
verify_email_schema = extend_schema(
    tags=["Register"],
    summary="Verification email via token",
    request=VerifyEmailSerializer, # <-- CORRECTION ICI
)

verify_otp_schema = extend_schema(
    tags=["Register"],
    summary="Verification OTP telephone",
    description="Contexte 'registration' = verification. Contexte 'login' = connexion avec tokens retournes.",
    request=VerifyOTPSerializer, # <-- CORRECTION ICI
)

# --- Password ---
forgot_password_schema = extend_schema(
    tags=["Password"],
    summary="Envoi lien de reinitialisation",
    description="Reponse generique meme si l'email n'existe pas (securite).",
    request=ForgotPasswordSerializer, # <-- CORRECTION ICI
)

reset_password_schema = extend_schema(
    tags=["Password"],
    summary="Reinitialisation via token",
    description="Reinitialise le mot de passe et revoque toutes les sessions.",
    request=ResetPasswordSerializer, # <-- CORRECTION ICI
)

change_password_schema = extend_schema(
    tags=["Password"],
    summary="Changement avec ancien mot de passe",
    description="Revoque toutes les sessions sauf la courante.",
    request=ChangePasswordSerializer, # <-- CORRECTION ICI
)

# --- 2FA ---
twofa_enable_schema = extend_schema(tags=["2FA"], summary="Activer 2FA - generer secret + QR code")
twofa_confirm_schema = extend_schema(tags=["2FA"], summary="Confirmer activation 2FA", request=TwoFAConfirmSerializer)
twofa_verify_schema = extend_schema(tags=["2FA"], summary="Challenge 2FA au login", description="Appele quand requires_2fa=true. Echange le temp_token + code contre un access_token.", request=TwoFAVerifySerializer)
twofa_disable_schema = extend_schema(tags=["2FA"], summary="Desactiver 2FA", request=TwoFADisableSerializer)

# --- Sessions ---
refresh_schema = extend_schema(
    tags=["Sessions"],
    summary="Rotation refresh token",
    description="Le refresh token est lu depuis le cookie HttpOnly. Un nouveau est emis (rotation).",
)

logout_schema = extend_schema(tags=["Sessions"], summary="Deconnexion", description="Revoque la session courante et supprime le cookie refresh_token.")

session_list_schema = extend_schema(tags=["Sessions"], summary="Lister sessions actives", responses={200: SessionResponseSerializer(many=True)})
session_revoke_schema = extend_schema(tags=["Sessions"], summary="Revoquer une session")

verify_token_schema = extend_schema(
    tags=["Sessions"],
    summary="Validation JWT (inter-services)",
    description="Endpoint interne. Effectue 6 verifications : signature, expiration, blocked, deactivated, platform active, session active.",
    responses={200: {"description": "Token valide"}, 401: {"description": "Token invalide avec raison"}},
)

token_exchange_schema = extend_schema(
    tags=["Sessions"],
    summary="Echange cookie vers Bearer",
    description="Apres callback OAuth/magic-link. Lit le cookie access_token et le retourne en JSON.",
)

# --- Profile ---
me_schema = extend_schema(tags=["Profile"], summary="Profil identite (sans roles)", description="Retourne l'identite pure. Les roles sont dans le Service Users.", responses={200: UserAuthResponseSerializer})
login_history_schema = extend_schema(tags=["Profile"], summary="Historique des connexions", responses={200: LoginHistoryResponseSerializer(many=True)})
user_stats_schema = extend_schema(tags=["Profile"], summary="Statistiques utilisateur")

# --- Admin ---
block_schema = extend_schema(tags=["Admin"], summary="Bloquer un utilisateur", description="Revoque toutes les sessions. Ne modifie pas le statut Users.")
unblock_schema = extend_schema(tags=["Admin"], summary="Debloquer un utilisateur")
deactivate_self_schema = extend_schema(tags=["Admin"], summary="Desactiver son propre compte", description="Mot de passe requis. Propage status-sync vers Users.", request=DeactivateAccountSerializer)
deactivate_admin_schema = extend_schema(tags=["Admin"], summary="Desactivation S2S (inter-service)", description="Appele par Users pour soft delete global sans mot de passe.")
purge_schema = extend_schema(tags=["Admin"], summary="Purge RGPD", description="Suppression physique irreversible. Transactionnel.")

# --- OAuth ---
oauth_google_init_schema = extend_schema(tags=["OAuth"], summary="Initier OAuth Google", parameters=[
    OpenApiParameter(name="platform_id", location=OpenApiParameter.QUERY, type=str),
    OpenApiParameter(name="redirect_uri", location=OpenApiParameter.QUERY, type=str),
])
oauth_google_callback_schema = extend_schema(tags=["OAuth"], summary="Callback OAuth Google")
oauth_facebook_init_schema = extend_schema(tags=["OAuth"], summary="Initier OAuth Facebook")
oauth_facebook_callback_schema = extend_schema(tags=["OAuth"], summary="Callback OAuth Facebook")

# --- Platforms ---
platform_list_create_schema = extend_schema(
    tags=["Platforms"], 
    summary="Creer ou lister les plateformes", 
    request=PlatformCreateSerializer, 
    responses={201: PlatformResponseSerializer, 200: PlatformResponseSerializer(many=True)}
)
platform_detail_schema = extend_schema(
    tags=["Platforms"], 
    summary="Modifier ou desactiver une plateforme",
    request=PlatformUpdateSerializer,
    responses={200: PlatformResponseSerializer}
)

# --- S2S ---
s2s_token_schema = extend_schema(
    tags=["S2S"], 
    summary="Generer token S2S", 
    description="Flux Client Credentials. Retourne un JWT S2S valide 1h.",
    request={"type": "object", "properties": {"client_id": {"type": "string"}, "client_secret": {"type": "string"}}}
)
s2s_introspect_schema = extend_schema(
    tags=["S2S"], 
    summary="Valider token S2S", 
    description="Permet a un service de verifier la validite d'un token S2S plateforme.",
    request={"type": "object", "properties": {"token": {"type": "string"}}}
)