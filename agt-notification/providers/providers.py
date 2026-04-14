"""AGT Notification Service v1.0 - Providers abstraction layer."""
import logging
from dataclasses import dataclass
from typing import List
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@dataclass
class SendResult:
    success: bool
    error: str = None
    provider_message_id: str = None


class BaseProvider:
    name = "base"

    def send(self, notification, user_data):
        raise NotImplementedError


class SendGridProvider(BaseProvider):
    name = "sendgrid"

    def send(self, notification, user_data):
        from django.conf import settings
        api_key = getattr(settings, "SENDGRID_API_KEY", "")
        if not api_key:
            logger.warning("SENDGRID_API_KEY non configure")
            return False
        email = (user_data or {}).get("email")
        if not email:
            return False
        try:
            import httpx
            resp = httpx.post("https://api.sendgrid.com/v3/mail/send", headers={
                "Authorization": f"Bearer {api_key}", "Content-Type": "application/json"
            }, json={
                "personalizations": [{"to": [{"email": email}]}],
                "from": {"email": getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@agt.com")},
                "subject": notification.subject or "Notification",
                "content": [{"type": "text/html", "value": notification.body}],
            }, timeout=10.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"SendGrid error: {e}")
            return False


class MailgunProvider(BaseProvider):
    name = "mailgun"

    def send(self, notification, user_data):
        logger.info(f"[MOCK] Mailgun send to {(user_data or {}).get('email')}")
        return False  # Fallback provider - implement when needed


class TwilioProvider(BaseProvider):
    name = "twilio"

    def send(self, notification, user_data):
        from django.conf import settings
        sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
        token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
        from_number = getattr(settings, "TWILIO_FROM_NUMBER", "")
        phone = (user_data or {}).get("phone")
        if not all([sid, token, from_number, phone]):
            return False
        try:
            import httpx
            resp = httpx.post(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
                              auth=(sid, token), data={
                                  "From": from_number, "To": phone, "Body": notification.body,
                              }, timeout=10.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Twilio error: {e}")
            return False


class VonageProvider(BaseProvider):
    name = "vonage"

    def send(self, notification, user_data):
        logger.info(f"[MOCK] Vonage send to {(user_data or {}).get('phone')}")
        return False


class FCMProvider(BaseProvider):
    name = "fcm"

    def send(self, notification, user_data):
        from django.conf import settings
        server_key = getattr(settings, "FCM_SERVER_KEY", "")
        if not server_key:
            return False
        from apps.devices.models import DeviceToken
        tokens = DeviceToken.objects.filter(user_id=notification.user_id, is_active=True, device_type__in=["android", "web"]).values_list("token", flat=True)
        if not tokens:
            return False
        try:
            import httpx
            for t in tokens:
                httpx.post("https://fcm.googleapis.com/fcm/send", headers={
                    "Authorization": f"key={server_key}", "Content-Type": "application/json"
                }, json={
                    "to": t, "notification": {"title": notification.subject or "Notification", "body": notification.body[:200]},
                }, timeout=10.0)
            return True
        except Exception as e:
            logger.error(f"FCM error: {e}")
            return False


class WhatsAppProvider(BaseProvider):
    name = "meta_whatsapp"

    def send(self, notification, user_data):
        logger.info(f"[MOCK] WhatsApp send to {(user_data or {}).get('phone')}")
        return False

class SMTPProvider(BaseProvider):
    """Envoie des emails via le serveur SMTP local (Mailpit en dev)."""
    name = "smtp_local"

    def send(self, notification, user_data):
        from django.conf import settings
        email = (user_data or {}).get("email")
        if not email:
            return False
        try:
            send_mail(
                subject=notification.subject or "Notification",
                message=notification.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=notification.body,
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"SMTP Error: {e}")
            return False

class ConsoleSMSProvider(BaseProvider):
    """Affiche le SMS dans les logs (Console) pour le dev."""
    name = "console_sms"

    def send(self, notification, user_data):
        phone = (user_data or {}).get("phone")
        print(f"\n--- [SMS CONSOLE] To: {phone} ---\n{notification.body}\n---------------------------\n")
        return True

# --- MODIFIE LA PROVIDER_MAP ---
PROVIDER_MAP = {
    "email": [SMTPProvider(), SendGridProvider()], # SMTP en premier pour le dev
    "sms": [ConsoleSMSProvider(), TwilioProvider()], # Console en premier
    "push": [FCMProvider()],
    "whatsapp": [WhatsAppProvider()],
    "in_app": [],
}


def get_providers(channel) -> List[BaseProvider]:
    return PROVIDER_MAP.get(channel, [])
