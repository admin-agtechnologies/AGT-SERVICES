"""AGT Notification Service v1.0 - Workers Celery : envoi, campagnes, scheduled."""
import logging
import time
import re
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=1, retry_backoff=True, name="notifications.send_notification")
def send_notification_task(self, notification_id):
    from apps.notifications.models import Notification, NotificationLog
    from apps.notifications.services import UserResolverService
    from providers.providers import get_providers

    try:
        notif = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    if notif.status != "pending":
        return

    user_data = UserResolverService.get_user(str(notif.user_id))
    if user_data and user_data.get("status") == "deleted":
        notif.mark_failed()
        return

    if notif.channel == "in_app":
        notif.mark_sent()
        return

    providers = get_providers(notif.channel)
    for attempt, provider in enumerate(providers, 1):
        try:
            success = provider.send(notif, user_data)
            NotificationLog.objects.create(notification=notif, channel=notif.channel, provider=provider.name,
                                            status="sent" if success else "failed", attempt=attempt)
            if success:
                notif.mark_sent()
                return
        except Exception as e:
            NotificationLog.objects.create(notification=notif, channel=notif.channel, provider=provider.name,
                                            status="failed", attempt=attempt, error_message=_mask(str(e)))

    if notif.category != "security":
        _try_fallback(notif, user_data)
    else:
        notif.mark_failed()


def _try_fallback(notif, user_data):
    from apps.notifications.models import PlatformChannelConfig, Notification
    from providers.providers import get_providers

    config = PlatformChannelConfig.get_for_platform(str(notif.platform_id))
    if not config.fallback_enabled:
        notif.mark_failed()
        return

    order = config.priority_order
    idx = order.index(notif.channel) if notif.channel in order else -1
    for ch in order[idx + 1:]:
        if ch == "in_app":
            Notification.objects.create(user_id=notif.user_id, platform_id=notif.platform_id, template=notif.template,
                                         channel="in_app", category=notif.category, subject=notif.subject,
                                         body=notif.body, status="sent", sent_at=timezone.now())
            notif.mark_failed()
            return
        for provider in get_providers(ch):
            try:
                if provider.send(notif, user_data):
                    notif.channel = ch
                    notif.mark_sent()
                    return
            except Exception:
                pass
    notif.mark_failed()


@shared_task(name="notifications.process_campaign")
def process_campaign_task(campaign_id):
    from apps.campaigns.models import Campaign, CampaignRecipient
    from apps.notifications.models import Notification

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return

    if campaign.status == "cancelled":
        return

    campaign.status = "running"
    campaign.started_at = timezone.now()
    campaign.save(update_fields=["status", "started_at"])

    recipients = CampaignRecipient.objects.filter(campaign=campaign, status="pending")
    delay = 1.0 / campaign.throttle_per_second if campaign.throttle_per_second > 0 else 0.1

    for r in recipients:
        campaign.refresh_from_db()
        if campaign.status == "cancelled":
            break
        try:
            rendered = campaign.template.render(r.variables or {}) if campaign.template else {"subject": None, "body": ""}
            notif = Notification.objects.create(user_id=r.user_id, platform_id=campaign.platform_id,
                                                 template=campaign.template, channel=campaign.channel,
                                                 category="marketing", subject=rendered.get("subject"),
                                                 body=rendered.get("body", ""), status="pending")
            r.notification = notif
            r.status = "sent"
            r.save(update_fields=["notification", "status"])
            send_notification_task.delay(str(notif.id))
            campaign.sent_count += 1
        except Exception as e:
            r.status = "failed"
            r.save(update_fields=["status"])
            campaign.failed_count += 1
        campaign.save(update_fields=["sent_count", "failed_count"])
        time.sleep(delay)

    if campaign.status != "cancelled":
        campaign.status = "completed"
        campaign.completed_at = timezone.now()
        campaign.save(update_fields=["status", "completed_at"])


@shared_task(name="notifications.process_scheduled")
def process_scheduled_notifications():
    from apps.notifications.models import ScheduledNotification, Notification
    now = timezone.now()
    pending = ScheduledNotification.objects.filter(status="pending", scheduled_at__lte=now)
    for sn in pending:
        try:
            rendered = sn.template.render(sn.variables or {}) if sn.template else {"subject": None, "body": ""}
            notif = Notification.objects.create(user_id=sn.user_id, platform_id=sn.platform_id,
                                                 template=sn.template, channel=sn.channel,
                                                 category="transactional", subject=rendered.get("subject"),
                                                 body=rendered.get("body", ""), status="pending")
            sn.notification = notif
            sn.status = "sent"
            sn.save(update_fields=["notification", "status", "updated_at"])
            send_notification_task.delay(str(notif.id))
        except Exception as e:
            logger.error(f"Scheduled {sn.id} failed: {e}")


def _mask(text):
    if not text:
        return text
    text = re.sub(r'[\w.-]+@[\w.-]+\.\w+', '[EMAIL]', text)
    text = re.sub(r'\+?[0-9]{8,15}', '[PHONE]', text)
    return text[:500]
