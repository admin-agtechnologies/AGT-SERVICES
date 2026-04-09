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

logger = logging.getLogger(__name__)


class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({"data": data, "page": self.page.number, "total": self.page.paginator.count})


# --- Health ---

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check")
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
        return Response({"status": "healthy" if db_ok and redis_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "version": "1.0.0"}, status=code)


# --- Plans ---

class PlanListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Plans"], summary="Creer un plan avec prix et quotas")
    def post(self, request):
        d = request.data
        platform_id = d.get("platform_id")
        slug = d.get("slug")
        if not all([platform_id, d.get("name"), slug]):
            return Response({"detail": "platform_id, name et slug requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Plan.objects.filter(platform_id=platform_id, slug=slug).exists():
            return Response({"detail": "Slug existe deja."}, status=status.HTTP_409_CONFLICT)

        plan = Plan.objects.create(
            platform_id=platform_id, name=d["name"], slug=slug,
            description=d.get("description"), is_free=d.get("is_free", False),
            is_default=d.get("is_default", False), tier_order=d.get("tier_order", 0),
            metadata=d.get("metadata"),
        )
        for p in d.get("prices", []):
            PlanPrice.objects.create(plan=plan, billing_cycle=p["billing_cycle"],
                                      cycle_days=p.get("cycle_days"), price=p["price"],
                                      currency=p.get("currency", "XAF"))
        for q in d.get("quotas", []):
            PlanQuota.objects.create(plan=plan, quota_key=q["quota_key"], limit_value=q["limit_value"],
                                      is_cyclical=q.get("is_cyclical", True),
                                      overage_policy=q.get("overage_policy", "hard"),
                                      overage_unit_price=q.get("overage_unit_price", 0))

        return Response({"id": str(plan.id), "name": plan.name, "slug": plan.slug, "message": "Plan created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Plans"], summary="Lister les plans")
    def get(self, request):
        qs = Plan.objects.filter(is_active=True)
        pid = request.GET.get("platform_id")
        if pid:
            qs = qs.filter(platform_id=pid)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = []
        for p in page:
            prices = [{"billing_cycle": pr.billing_cycle, "price": float(pr.price), "currency": pr.currency} for pr in p.prices.filter(is_active=True)]
            quotas = [{"quota_key": q.quota_key, "limit_value": q.limit_value, "overage_policy": q.overage_policy} for q in p.quotas.all()]
            data.append({"id": str(p.id), "platform_id": str(p.platform_id), "name": p.name, "slug": p.slug,
                         "is_free": p.is_free, "tier_order": p.tier_order, "prices": prices, "quotas": quotas})
        return paginator.get_paginated_response(data)


class PlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Plans"], summary="Detail d'un plan")
    def get(self, request, plan_id):
        try:
            p = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan introuvable."}, status=status.HTTP_404_NOT_FOUND)
        prices = [{"id": str(pr.id), "billing_cycle": pr.billing_cycle, "price": float(pr.price), "currency": pr.currency} for pr in p.prices.filter(is_active=True)]
        quotas = [{"quota_key": q.quota_key, "limit_value": q.limit_value, "is_cyclical": q.is_cyclical, "overage_policy": q.overage_policy, "overage_unit_price": float(q.overage_unit_price)} for q in p.quotas.all()]
        return Response({"id": str(p.id), "name": p.name, "slug": p.slug, "description": p.description,
                         "is_free": p.is_free, "tier_order": p.tier_order, "prices": prices, "quotas": quotas})

    @extend_schema(tags=["Plans"], summary="Modifier un plan (nom/description uniquement si actif)")
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

    @extend_schema(tags=["Plans"], summary="Archiver un plan")
    def post(self, request, plan_id):
        try:
            p = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"detail": "Plan introuvable."}, status=status.HTTP_404_NOT_FOUND)
        p.is_active = False
        p.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "Plan archived", "is_active": False})


# --- Subscriptions ---

class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Subscriptions"], summary="Creer un abonnement")
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

    @extend_schema(tags=["Subscriptions"], summary="Lister les abonnements")
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

    @extend_schema(tags=["Subscriptions"], summary="Detail abonnement avec usage quotas")
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

    @extend_schema(tags=["Subscriptions"], summary="Annuler (actif jusqu'a fin cycle)")
    def post(self, request, sub_id):
        sub, err = SubscriptionService.cancel(sub_id)
        if err:
            return Response({"detail": err}, status=status.HTTP_404_NOT_FOUND if err == "not_found" else status.HTTP_409_CONFLICT)
        return Response({"id": str(sub.id), "status": sub.status, "cancel_at_period_end": True, "message": "Subscription will cancel at period end"})


class SubscriptionChangePlanView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Subscriptions"], summary="Upgrade/downgrade avec prorata")
    def post(self, request, sub_id):
        d = request.data
        result, err = SubscriptionService.change_plan(sub_id, d.get("new_plan_id"), d.get("billing_cycle", "monthly"))
        if err:
            codes = {"not_found": 404, "same_plan": 400, "new_plan_not_found": 404, "subscription_not_active": 409}
            return Response({"detail": err}, status=codes.get(err, 400))
        return Response({**result, "message": "Plan changed"})


class SubscriptionActivateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Subscriptions"], summary="Activer apres paiement")
    def post(self, request, sub_id):
        sub, err = SubscriptionService.activate(sub_id)
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"id": str(sub.id), "status": sub.status, "message": "Subscription activated"})


class SubscriptionReactivateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Subscriptions"], summary="Reactiver un abonnement")
    def post(self, request, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "Introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if sub.status not in ["suspended", "expired", "cancelled"]:
            return Response({"detail": "Ne peut pas etre reactive."}, status=status.HTTP_409_CONFLICT)
        sub.status = "active"
        sub.cancel_at_period_end = False
        sub.cancelled_at = None
        sub.save(update_fields=["status", "cancel_at_period_end", "cancelled_at", "updated_at"])
        SubscriptionEvent.objects.create(subscription=sub, event_type="reactivated")
        return Response({"id": str(sub.id), "status": "active", "message": "Subscription reactivated"})


# --- Quotas ---

class QuotaCheckView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Quotas"], summary="Verifier quota (S2S, < 50ms)")
    def post(self, request):
        d = request.data
        result = QuotaService.check(d.get("platform_id"), d.get("subscriber_type", "user"),
                                     d.get("subscriber_id"), d.get("quota_key"), d.get("requested", 1))
        return Response(result)


class QuotaIncrementView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Quotas"], summary="Reporter consommation (S2S)")
    def post(self, request):
        d = request.data
        result, err = QuotaService.increment(d.get("platform_id"), d.get("subscriber_type", "user"),
                                              d.get("subscriber_id"), d.get("quota_key"), d.get("amount", 1))
        if err:
            code = 403 if err == "hard_limit_exceeded" else 404
            return Response({"detail": err}, status=code)
        return Response(result)


class QuotaReserveView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Quotas"], summary="Reserver quota (atomique)")
    def post(self, request):
        d = request.data
        result, err = QuotaService.reserve(d.get("platform_id"), d.get("subscriber_type", "user"),
                                            d.get("subscriber_id"), d.get("quota_key"),
                                            d.get("amount", 1), d.get("ttl_seconds", 300))
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)


class QuotaConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Quotas"], summary="Confirmer reservation")
    def post(self, request):
        result, err = QuotaService.confirm_reservation(request.data.get("reservation_id"))
        if err:
            return Response({"detail": err}, status=status.HTTP_404_NOT_FOUND)
        return Response(result)


class QuotaReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Quotas"], summary="Liberer reservation")
    def post(self, request):
        result, err = QuotaService.release_reservation(request.data.get("reservation_id"))
        if err:
            return Response({"detail": err}, status=status.HTTP_404_NOT_FOUND)
        return Response(result)


class QuotaUsageView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Quotas"], summary="Consultation usage courant")
    def get(self, request, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return Response({"detail": "Introuvable."}, status=status.HTTP_404_NOT_FOUND)
        usage = SubscriptionQuotaUsage.objects.filter(subscription=sub, period_start=sub.current_period_start)
        plan_quotas = {q.quota_key: {"limit": q.limit_value, "policy": q.overage_policy} for q in PlanQuota.objects.filter(plan=sub.plan)}
        data = []
        for u in usage:
            pq = plan_quotas.get(u.quota_key, {})
            data.append({"quota_key": u.quota_key, "used": u.used, "limit": pq.get("limit", 0),
                         "remaining": max(0, pq.get("limit", 0) - u.used), "overage": u.overage, "policy": pq.get("policy", "hard")})
        return Response({"subscription_id": str(sub.id), "quotas": data})


# --- Organizations ---

class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Organizations"], summary="Creer une organisation")
    def post(self, request):
        d = request.data
        if not all([d.get("platform_id"), d.get("name"), d.get("owner_user_id")]):
            return Response({"detail": "platform_id, name et owner_user_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        org = Organization.objects.create(platform_id=d["platform_id"], name=d["name"], owner_user_id=d["owner_user_id"])
        OrganizationMember.objects.create(organization=org, user_id=d["owner_user_id"], role="owner")
        return Response({"id": str(org.id), "name": org.name, "message": "Organization created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Organizations"], summary="Lister les organisations")
    def get(self, request):
        qs = Organization.objects.filter(is_active=True)
        pid = request.GET.get("platform_id")
        if pid:
            qs = qs.filter(platform_id=pid)
        data = [{"id": str(o.id), "name": o.name, "owner_user_id": str(o.owner_user_id)} for o in qs]
        return Response({"data": data})


class OrganizationMemberView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Organizations"], summary="Ajouter un membre")
    def post(self, request, org_id):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "user_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Organisation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        _, created = OrganizationMember.objects.get_or_create(organization=org, user_id=user_id)
        return Response({"message": "Member added" if created else "Already member"}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @extend_schema(tags=["Organizations"], summary="Lister les membres")
    def get(self, request, org_id):
        members = OrganizationMember.objects.filter(organization_id=org_id)
        data = [{"user_id": str(m.user_id), "role": m.role, "joined_at": m.joined_at.isoformat()} for m in members]
        return Response({"data": data})

    @extend_schema(tags=["Organizations"], summary="Retirer un membre")
    def delete(self, request, org_id, user_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"detail": "Organisation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if str(org.owner_user_id) == str(user_id):
            return Response({"detail": "Impossible de retirer le owner."}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = OrganizationMember.objects.filter(organization_id=org_id, user_id=user_id).delete()
        if not deleted:
            return Response({"detail": "Membre introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Member removed"})


# --- Platform Config ---

class PlatformConfigView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Config"], summary="Lire config plateforme")
    def get(self, request, platform_id):
        config = PlatformSubscriptionConfig.get_for_platform(str(platform_id))
        return Response({"platform_id": str(platform_id), "default_trial_days": config.default_trial_days,
                         "grace_period_days": config.grace_period_days, "post_trial_behavior": config.post_trial_behavior,
                         "default_currency": config.default_currency, "allowed_cycles": config.allowed_cycles})

    @extend_schema(tags=["Config"], summary="Modifier config plateforme")
    def put(self, request, platform_id):
        config, _ = PlatformSubscriptionConfig.objects.get_or_create(
            platform_id=platform_id, defaults={"allowed_cycles": ["monthly", "yearly"]})
        d = request.data
        for f in ["default_trial_days", "grace_period_days", "post_trial_behavior", "default_currency", "allowed_cycles", "require_default_plan"]:
            if f in d:
                setattr(config, f, d[f])
        config.save()
        return Response({"message": "Config updated"})


# --- Admin Stats ---

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Admin"], summary="Statistiques abonnements")
    def get(self, request):
        from django.db.models import Count, Sum
        total = Subscription.objects.count()
        by_status = dict(Subscription.objects.values_list("status").annotate(c=Count("id")))
        active = Subscription.objects.filter(status__in=["active", "trial"]).count()
        return Response({"total": total, "active": active, "by_status": by_status})
