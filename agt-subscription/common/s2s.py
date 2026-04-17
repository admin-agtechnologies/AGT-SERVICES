"""AGT Subscription Service v1.0 - Service-to-Service token management.

Ce module gère l'obtention et le cache du token S2S que Subscription
utilise pour s'authentifier auprès des autres services (Payment, Notification).

Pattern validé AGT — ne pas modifier la structure de ce fichier.
"""
import httpx
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


class S2STokenService:
    """Obtient et met en cache le token S2S depuis Auth Service.

    Le token est mis en cache Redis avec une marge de 60s avant expiration
    pour éviter d'envoyer un token expiré lors d'appels inter-services.
    """

    CACHE_KEY = "subscription_s2s_token"
    MARGIN_SECONDS = 60

    @staticmethod
    def get_token() -> str:
        """Retourne un token S2S valide, depuis le cache ou via Auth Service.

        Retourne une chaîne vide si la configuration S2S est absente
        (comportement non bloquant — le service reste opérationnel en mode dégradé).
        """
        cached = cache.get(S2STokenService.CACHE_KEY)
        if cached:
            return cached

        auth_url = getattr(settings, "S2S_AUTH_URL", "")
        client_id = getattr(settings, "S2S_CLIENT_ID", "")
        client_secret = getattr(settings, "S2S_CLIENT_SECRET", "")

        # Si les variables S2S ne sont pas configurées, on ne bloque pas le service
        if not all([auth_url, client_id, client_secret]):
            logger.warning("S2S non configuré — appels inter-services désactivés.")
            return ""

        try:
            resp = httpx.post(
                f"{auth_url}/auth/s2s/token",
                json={"client_id": client_id, "client_secret": client_secret},
                timeout=5.0,
            )

            if resp.status_code != 200:
                logger.error("S2S token fetch failed: %s %s", resp.status_code, resp.text)
                return ""

            data = resp.json()
            token = data.get("access_token", "")
            expires_in = data.get("expires_in", 3600)

            # On stocke avec une marge pour ne jamais envoyer un token sur le point d'expirer
            ttl = max(expires_in - S2STokenService.MARGIN_SECONDS, 60)
            cache.set(S2STokenService.CACHE_KEY, token, timeout=ttl)
            return token

        except Exception as e:
            logger.error("S2S token error: %s", str(e))
            return ""