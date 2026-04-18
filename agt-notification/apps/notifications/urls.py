from django.urls import path

from apps.notifications.views import (
    HealthCheckView, SendNotificationView, SendBulkNotificationView,
    PreferenceView, InAppListView, InAppUnreadCountView, InAppMarkReadView,
    InAppMarkAllReadView, InAppDeleteView, NotificationStatsView,
    NotificationLogsView, ChannelConfigView,
    ScheduleNotificationView, ScheduledNotificationListView, ScheduledNotificationDetailView,
)
from apps.campaigns.views import CampaignListCreateView, CampaignDetailView, CampaignProgressView, CampaignCancelView, CampaignStatsView

urlpatterns = [
    path("health", HealthCheckView.as_view(), name="health"),
    path("notifications/send", SendNotificationView.as_view(), name="notif-send"),
    path("notifications/send-bulk", SendBulkNotificationView.as_view(), name="notif-send-bulk"),
    path("notifications/stats", NotificationStatsView.as_view(), name="notif-stats"),
    path("notifications/logs", NotificationLogsView.as_view(), name="notif-logs"),
    path("users/<str:user_id>/notification-preferences", PreferenceView.as_view(), name="prefs"),
    path("users/<str:user_id>/notifications", InAppListView.as_view(), name="inapp-list"),
    path("users/<str:user_id>/notifications/unread-count", InAppUnreadCountView.as_view(), name="inapp-unread"),
    path("users/<str:user_id>/notifications/read-all", InAppMarkAllReadView.as_view(), name="inapp-read-all"),
    path("users/<str:user_id>/notifications/<uuid:notification_id>/read", InAppMarkReadView.as_view(), name="inapp-read"),
    path("users/<str:user_id>/notifications/<uuid:notification_id>", InAppDeleteView.as_view(), name="inapp-delete"),
    path("platforms/<str:platform_id>/channels-priority", ChannelConfigView.as_view(), name="channel-config"),
    path("notifications/schedule", ScheduleNotificationView.as_view(), name="notif-schedule"),
    path("notifications/scheduled", ScheduledNotificationListView.as_view(), name="notif-scheduled-list"),
    path("notifications/scheduled/<uuid:scheduled_id>", ScheduledNotificationDetailView.as_view(), name="notif-scheduled-detail"),
]
