"""AGT Subscription Service v1.0 - Views."""
import logging
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema

from apps.plans.models import Plan, PlanPrice, PlanQuota
from apps.subscriptions.models import (
    Subscription, SubscriptionEvent, SubscriptionQuotaUsage, PlatformSubscriptionConfig,
)
from apps.organizations.models import Organization, OrganizationMember
from apps.subscriptions.service import SubscriptionService
from apps.quotas.service import QuotaService

# Import des décorateurs Swagger — request + responses documentés pour chaque endpoint
from apps.subscriptions.swagger import (
    health_schema,
    plan_create_schema, plan_list_schema, plan_detail_schema,
    plan_update_schema, plan_archive_schema,
    subscription_create_schema, subscription_list_schema, subscription_detail_schema,
    subscription_activate_schema, subscription_cancel_schema,
    subscription_change_plan_schema, subscription_reactivate_schema,
    quota_check_schema, quota_increment_schema, quota_reserve_schema,
    quota_confirm_schema, quota_release_schema, quota_usage_schema,
    organization_create_schema, organization_list_schema,
    member_add_schema, member_list_schema, member_remove_schema,
    config_get_schema, config_update_schema,
)

logger = logging.getLogger(__name__)


class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({"data": data, "page": self.page.number, "total": self.page.paginator.count})


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @health_schema
    def get(self, request):
        db_ok = redis_ok = True
        try:
            from django.db import connection
            connection.ensure_connection()
        except Exception:
            db_ok = False
        try:
            from django.core.cache import cache
            cache.set("health", "ok", 5)
            redis_ok = cache.get("health") == "ok"
        except Exception:
            redis_ok = False
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            "status": "healthy" if db_ok and redis_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "version": "1.0.0",
        }, status=code)


# ---------------------------------------------------------------------------
# Plans
# ---------------------------------------------------------------------------

class PlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @plan_create_schema
    def post(self, request):
        d = request.data
        platform_id = d.get("platform_id")
        slug = d.get("slug")
        if not all([platform_id, d.get("name"), slug]):
            return Response({"detail": "platform_id, name et slug requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Plan.objects.filter(platform_id=platform_id, slug=slug).exists():
            return Response({"detail": "Slug existe deja pour cette plateforme."}, status=status.HTTP_409_CONFLICT)

        plan = Plan.objects.create(
            platform_id=platform_id,
            name=d["name"],
            slug=slug,
            description=d.get("description"),
            is_free=d.get("is_free", False),
            is_default=d.get("is_default", False),
            tier_order=d.get("tier_order", 0),
            metadata=d.get("metadata"),
        )

        for price_data in d.get("prices", []):
            PlanPrice.objects.create(
                plan=plan,
                billing_cycle=price_data["billing_cycle"],
                price=price_data["price"],
                currency=price_data.get("currency", "XAF"),
                cycle_days=price_data.get("cycle_days"),
            )

        for quota_data in d.get("quotas", []):
            PlanQuota.objects.create(
                plan=plan,
                quota_key=quota_data["quota_key"],
                limit_value=quota_data["limit_value"],
                is_cyclical=quota_data.get("is_cyclical", True),
                overage_policy=quota_data.get("overage_policy", "hard"),
                overage_unit_price=quota_data.get("overage_unit_price", 0),
            )

        prices = [{"id": str(pr.id), "billing_cycle": pr.billing_cycle, "price": float(pr.price), "currency": pr.currency}
                  for pr in plan.prices.filter(is_active=True)]
        quotas = [{"quota_key": q.quota_key, "limit_value": q.limit_value, "is_cyclical": q.is_cyclical,
                   "overage_policy": q.overage_policy, "overage_unit_price": float(q.overage_unit_price)}
                  for q in plan.quotas.all()]
        return Response({
            "id": str(plan.id), "name": plan.name, "slug": plan.slug,
            "description": plan.description, "is_free": plan.is_free,
            "tier_order": plan.tier_order, "prices": prices, "quotas": quotas,
        }, status=status.HTTP_201_CREATED)

    @plan_list_schema
    def get(self, request):
        qs = Plan.objects.prefetch_related("prices", "quotas").filter(is_active=True)
        platform_id = request.GET.get("platform_id")
        if platform_id:
            qs = qs.filter(platform_id=platform_id)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(p.id), "name": p.name, "slug": p.slug, "is_free": p.is_free,
                 "tier_order": p.tier_order, "platform_id": str(p.platform_id)} for p in page]
        return paginator.get_paginated_response(data)


class PlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @plan_detail_schema
    def get(self, request, plan_id):
        try:
            p = Plan.objects.prefetch_related("prices", "quotas").get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan introuvable."}, status=status.HTTP_404_NOT_FOUND)
        prices = [{"id": str(pr.id), "billing_cycle": pr.billing_cycle, "price": float(pr.price), "currency": pr.currency}
                  for pr in p.prices.filter(is_active=True)]
        quotas = [{"quota_key": q.quota_key, "limit_value": q.limit_value, "is_cyclical": q.is_cyclical,
                   "overage_policy": q.overage_policy, "overage_unit_price": float(q.overage_unit_price)}
                  for q in p.quotas.all()]
        return Response({
            "id": str(p.id), "name": p.name, "slug": p.slug, "description": p.description,
            "is_free": p.is_free, "tier_order": p.tier_order, "prices": prices, "quotas": quotas,
        })

    @plan_update_schema
    def put(self, request, plan_id):
        try:
            p = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan introuvable."}, status=status.HTTP_404_NOT_FOUND)
        d = request.data
        if "name" in d:
            p.name = d["name"]
        if "description" in d:
            p.description = d["description"]
        if "metadata" in d:
            p.metadata = d["metadata"]
        p.save()
        return Response({"id": str(p.id), "name": p.name, "message": "Plan updated"})


class PlanArchiveView(APIView):
    permission_classes = [IsAuthenticated]

    @plan_archive_schema
    def post(self, request, plan_id):
        try:
            p = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if p.has_active_subscriptions():
            return Response({"detail": "Plan avec abonnements actifs."}, status=status.HTTP_409_CONFLICT)
        p.is_active = False
        p.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "Plan archived", "is_active": False})


# ---------------------------------------------------------------------------
# Subscriptions
# ---------------------------------------------------------------------------

class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_create_schema
    def post(self, request):
        d = request.data
        sub, err = SubscriptionService.create(
            d.get("platform_id"), d.get("subscriber_type", "user"), d.get("subscriber_id"),
            d.get("plan_id"), d.get("billing_cycle", "monthly"), d.get("with_trial", False),
        )
        if err:
            codes = {"active_subscription_exists": 409, "plan_not_found": 404, "price_not_found": 400}
            return Response({"detail": err}, status=codes.get(err, 400))
        return Response({
            "id": str(sub.id), "status": sub.status, "plan": sub.plan.name,
            "current_period_start": sub.current_period_start.isoformat(),
            "current_period_end": sub.current_period_end.isoformat(),
            "trial_end": sub.trial_end.isoformat() if sub.trial_end else None,
            "message": "Subscription created",
        }, status=status.HTTP_201_CREATED)


class SubscriptionListView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_list_schema
    def get(self, request):
        qs = Subscription.objects.select_related("plan").all()
        for f in ["platform_id", "subscriber_id", "status"]:
            v = request.GET.get(f)
            if v:
                qs = qs.filter(**{f: v})
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(s.id), "plan": s.plan.name, "status": s.status,
                 "subscriber_type": s.subscriber_type, "subscriber_id": str(s.subscriber_id),
                 "current_period_end": s.current_period_end.isoformat()} for s in page]
        return paginator.get_paginated_response(data)


class SubscriptionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_detail_schema
    def get(self, request, sub_id):
        try:
            s = Subscription.objects.select_related("plan", "plan_price").get(id=sub_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "Abonnement introuvable."}, status=status.HTTP_404_NOT_FOUND)
        usage = SubscriptionQuotaUsage.objects.filter(subscription=s, period_start=s.current_period_start)
        quotas = [{"quota_key": u.quota_key, "used": u.used, "overage": u.overage} for u in usage]
        plan_quotas = {q.quota_key: q.limit_value for q in PlanQuota.objects.filter(plan=s.plan)}
        for q in quotas:
            q["limit"] = plan_quotas.get(q["quota_key"], 0)
        return Response({
            "id": str(s.id), "plan": {"id": str(s.plan.id), "name": s.plan.name},
            "status": s.status, "billing_cycle": s.plan_price.billing_cycle,
            "current_period_start": s.current_period_start.isoformat(),
            "current_period_end": s.current_period_end.isoformat(),
            "trial_end": s.trial_end.isoformat() if s.trial_end else None,
            "cancel_at_period_end": s.cancel_at_period_end,
            "quotas_usage": quotas,
        })


class SubscriptionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_cancel_schema
    def post(self, request, sub_id):
        sub, err = SubscriptionService.cancel(sub_id)
        if err:
            return Response({"detail": err},
                            status=status.HTTP_404_NOT_FOUND if err == "not_found" else status.HTTP_409_CONFLICT)
        return Response({"id": str(sub.id), "status": sub.status, "cancel_at_period_end": True,
                         "message": "Subscription will cancel at period end"})


class SubscriptionChangePlanView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_change_plan_schema
    def post(self, request, sub_id):
        d = request.data
        result, err = SubscriptionService.change_plan(sub_id, d.get("new_plan_id"), d.get("billing_cycle", "monthly"))
        if err:
            codes = {"not_found": 404, "same_plan": 400, "new_plan_not_found": 404, "subscription_not_active": 409}
            return Response({"detail": err}, status=codes.get(err, 400))
        return Response({**result, "message": "Plan changed"})


class SubscriptionActivateView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_activate_schema
    def post(self, request, sub_id):
        sub, err = SubscriptionService.activate(sub_id)
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"id": str(sub.id), "status": sub.status, "message": "Subscription activated"})


class SubscriptionReactivateView(APIView):
    permission_classes = [IsAuthenticated]

    @subscription_reactivate_schema
    def post(self, request, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "Introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if sub.status not in ["active", "cancelled"]:
            return Response({"detail": "Reactivation impossible dans cet etat."}, status=status.HTTP_409_CONFLICT)
        sub.status = "active"
        sub.cancel_at_period_end = False
        sub.cancelled_at = None
        sub.save(update_fields=["status", "cancel_at_period_end", "cancelled_at"])
        return Response({"id": str(sub.id), "status": sub.status, "message": "Subscription reactivated"})


# ---------------------------------------------------------------------------
# Quotas
# ---------------------------------------------------------------------------

class QuotaCheckView(APIView):
    permission_classes = [IsAuthenticated]

    @quota_check_schema
    def post(self, request):
        d = request.data
        # check() retourne un dict simple (toujours 200, allowed=False si pas de sub)
        result = QuotaService.check(
            d.get("platform_id"),
            d.get("subscriber_type", "user"),
            d.get("subscriber_id"),
            d.get("quota_key"),
            d.get("amount", d.get("requested", 1)),
        )
        return Response(result)


class QuotaIncrementView(APIView):
    permission_classes = [IsAuthenticated]

    @quota_increment_schema
    def post(self, request):
        d = request.data
        result, err = QuotaService.increment(
            d.get("platform_id"),
            d.get("subscriber_type", "user"),
            d.get("subscriber_id"),
            d.get("quota_key"),
            d.get("amount", 1),
        )
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class QuotaReserveView(APIView):
    permission_classes = [IsAuthenticated]

    @quota_reserve_schema
    def post(self, request):
        d = request.data
        result, err = QuotaService.reserve(
            d.get("platform_id"),
            d.get("subscriber_type", "user"),
            d.get("subscriber_id"),
            d.get("quota_key"),
            d.get("amount", 1),
        )
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)


class QuotaConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    @quota_confirm_schema
    def post(self, request):
        result, err = QuotaService.confirm_reservation(request.data.get("reservation_id"))
        if err:
            return Response({"detail": err}, status=status.HTTP_404_NOT_FOUND)
        return Response(result)


class QuotaReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    @quota_release_schema
    def post(self, request):
        result, err = QuotaService.release_reservation(request.data.get("reservation_id"))
        if err:
            return Response({"detail": err}, status=status.HTTP_404_NOT_FOUND)
        return Response(result)


class QuotaUsageView(APIView):
    permission_classes = [IsAuthenticated]

    @quota_usage_schema
    def get(self, request, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "Introuvable."}, status=status.HTTP_404_NOT_FOUND)
        usage = SubscriptionQuotaUsage.objects.filter(subscription=sub, period_start=sub.current_period_start)
        plan_quotas = {q.quota_key: {"limit": q.limit_value, "policy": q.overage_policy}
                       for q in PlanQuota.objects.filter(plan=sub.plan)}
        data = []
        for u in usage:
            pq = plan_quotas.get(u.quota_key, {})
            data.append({
                "quota_key": u.quota_key, "used": u.used,
                "limit": pq.get("limit", 0),
                "remaining": max(0, pq.get("limit", 0) - u.used),
                "overage": u.overage, "policy": pq.get("policy", "hard"),
            })
        return Response({"subscription_id": str(sub.id), "quotas": data})


# ---------------------------------------------------------------------------
# Organizations
# ---------------------------------------------------------------------------

class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @organization_create_schema
    def post(self, request):
        d = request.data
        if not all([d.get("platform_id"), d.get("name"), d.get("owner_user_id")]):
            return Response({"detail": "platform_id, name et owner_user_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        if Organization.objects.filter(platform_id=d["platform_id"], name=d["name"]).exists():
            return Response({"detail": "Organisation existe deja."}, status=status.HTTP_409_CONFLICT)
        org = Organization.objects.create(
            platform_id=d["platform_id"], name=d["name"], owner_user_id=d["owner_user_id"]
        )
        OrganizationMember.objects.create(organization=org, user_id=d["owner_user_id"], role="owner")
        return Response({
            "id": str(org.id), "platform_id": str(org.platform_id),
            "name": org.name, "owner_user_id": str(org.owner_user_id), "is_active": org.is_active,
        }, status=status.HTTP_201_CREATED)

    @organization_list_schema
    def get(self, request):
        qs = Organization.objects.filter(is_active=True)
        platform_id = request.GET.get("platform_id")
        if platform_id:
            qs = qs.filter(platform_id=platform_id)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(o.id), "name": o.name, "platform_id": str(o.platform_id),
                 "owner_user_id": str(o.owner_user_id)} for o in page]
        return paginator.get_paginated_response(data)


class OrganizationMemberView(APIView):
    permission_classes = [IsAuthenticated]

    @member_add_schema
    def post(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Organisation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        user_id = request.data.get("user_id")
        role = request.data.get("role", "member")
        if not user_id:
            return Response({"detail": "user_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        if OrganizationMember.objects.filter(organization=org, user_id=user_id).exists():
            return Response({"detail": "Utilisateur deja membre."}, status=status.HTTP_409_CONFLICT)
        member = OrganizationMember.objects.create(organization=org, user_id=user_id, role=role)
        return Response({"id": str(member.id), "user_id": str(member.user_id), "role": member.role},
                        status=status.HTTP_201_CREATED)

    @member_list_schema
    def get(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Organisation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        members = org.members.all()
        data = [{"id": str(m.id), "user_id": str(m.user_id), "role": m.role,
                 "joined_at": m.joined_at.isoformat()} for m in members]
        return Response({"organization_id": str(org.id), "members": data})

    @member_remove_schema
    def delete(self, request, org_id, user_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Organisation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        deleted, _ = OrganizationMember.objects.filter(organization=org, user_id=user_id).delete()
        if not deleted:
            return Response({"detail": "Membre introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Platform Config
# ---------------------------------------------------------------------------

class PlatformConfigView(APIView):
    permission_classes = [IsAuthenticated]

    @config_get_schema
    def get(self, request, platform_id):
        config, _ = PlatformSubscriptionConfig.objects.get_or_create(platform_id=platform_id)
        return Response({
            "platform_id": str(config.platform_id),
            "trial_days": config.default_trial_days,
            "grace_period_days": config.grace_period_days,
            "allowed_cycles": config.allowed_cycles,
            "default_currency": config.default_currency,
        })

    @config_update_schema
    def put(self, request, platform_id):
        config, _ = PlatformSubscriptionConfig.objects.get_or_create(platform_id=platform_id)
        d = request.data
        for field in ["default_trial_days", "grace_period_days", "allowed_cycles", "default_currency"]:
            if field in d:
                setattr(config, field, d[field])
        config.save()
        return Response({
            "platform_id": str(config.platform_id),
            "trial_days": config.default_trial_days,
            "grace_period_days": config.grace_period_days,
            "allowed_cycles": config.allowed_cycles,
            "default_currency": config.default_currency,
            "message": "Config updated",
        })


# ---------------------------------------------------------------------------
# Admin Stats
# ---------------------------------------------------------------------------

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Admin"], summary="Statistiques globales")
    def get(self, request):
        return Response({
            "total_plans": Plan.objects.filter(is_active=True).count(),
            "total_subscriptions": Subscription.objects.count(),
            "active_subscriptions": Subscription.objects.filter(status="active").count(),
            "total_organizations": Organization.objects.filter(is_active=True).count(),
        })