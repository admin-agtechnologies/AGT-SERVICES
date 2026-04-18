"""
AGT Subscription Service v1.0 - Configuration Celery.

Crons (Celery Beat) requis par le CDC :
- Renouvellement automatique des abonnements arrivant à expiration
- Passage en grace puis expired des abonnements non renouvelés
- Expiration des quota_reservations en pending depuis trop longtemps
- Alertes quota à 80% vers Notification
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("subscription")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Découverte automatique des tâches dans workers/tasks.py
app.conf.imports = ["workers.tasks"]

# ---------------------------------------------------------------------------
# Planification des crons Beat (CDC NF-12)
# ---------------------------------------------------------------------------
app.conf.beat_schedule = {

    # Toutes les heures : tenter le renouvellement des abonnements
    # dont current_period_end est dans moins de 24h
    "renew-expiring-subscriptions": {
        "task": "workers.tasks.renew_expiring_subscriptions",
        "schedule": crontab(minute=0),  # Toutes les heures
    },

    # Toutes les heures : passer les abonnements expirés en grace ou expired
    "process-expired-subscriptions": {
        "task": "workers.tasks.process_expired_subscriptions",
        "schedule": crontab(minute=15),  # Décalé de 15min par rapport au renouvellement
    },

    # Toutes les 10 minutes : expirer les quota_reservations pending trop vieilles
    "expire-stale-quota-reservations": {
        "task": "workers.tasks.expire_stale_quota_reservations",
        "schedule": crontab(minute="*/10"),
    },

    # Toutes les heures : envoyer alertes quota à 80% vers Notification
    "send-quota-alerts": {
        "task": "workers.tasks.send_quota_alerts",
        "schedule": crontab(minute=30),
    },
}

app.conf.timezone = "UTC"