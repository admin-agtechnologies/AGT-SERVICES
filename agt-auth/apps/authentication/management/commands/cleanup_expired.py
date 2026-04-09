"""
Commande Django : purge des données expirées.
Usage : python manage.py cleanup_expired
Cron quotidien recommandé.
"""
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

from apps.authentication.models import Session, RefreshToken, VerificationToken


class Command(BaseCommand):
    help = "Purge les sessions expirées, refresh tokens révoqués et verification tokens expirés."

    def handle(self, *args, **options):
        now = timezone.now()

        sessions_deleted, _ = Session.objects.filter(expires_at__lt=now).delete()

        rt_deleted, _ = RefreshToken.objects.filter(
            models.Q(expires_at__lt=now) | models.Q(is_revoked=True)
        ).delete()

        vt_deleted, _ = VerificationToken.objects.filter(
            models.Q(expires_at__lt=now) | models.Q(used_at__isnull=False)
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Nettoyage : sessions={sessions_deleted}, refresh_tokens={rt_deleted}, verification_tokens={vt_deleted}"
        ))
