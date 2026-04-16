"""AGT Wallet Service v1.0 - Views."""
import logging
from decimal import Decimal
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.accounts.models import Account, AccountStatus, LedgerTransaction, LedgerEntry, Hold, SplitRule
from apps.ledger.service import LedgerService
from rest_framework import serializers

class CreditSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(default="XAF")
    platform_id = serializers.UUIDField(required=False, allow_null=True)
    source = serializers.CharField(default="payment")
    source_reference_id = serializers.CharField(required=False, allow_null=True)
    idempotency_key = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)

class TransferSerializer(serializers.Serializer):
    from_account_id = serializers.UUIDField()
    to_account_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(default="XAF")
    platform_id = serializers.UUIDField(required=False, allow_null=True)
    idempotency_key = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)

class HoldSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    reason = serializers.CharField()
    idempotency_key = serializers.CharField()
    ttl_seconds = serializers.IntegerField(default=3600, required=False)
    source_reference_id = serializers.CharField(required=False, allow_null=True)

class SplitSerializer(serializers.Serializer):
    source_account_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(default="XAF")
    platform_id = serializers.UUIDField(required=False, allow_null=True)
    targets = serializers.ListField(child=serializers.DictField())
    idempotency_key = serializers.CharField()
    source_reference_id = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)

class DebitSerializer(serializers.Serializer):
    account_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(default="XAF")
    platform_id = serializers.UUIDField(required=False, allow_null=True)
    source = serializers.CharField(default="platform")
    source_reference_id = serializers.CharField(required=False, allow_null=True)
    idempotency_key = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)

logger = logging.getLogger(__name__)


class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    def get_paginated_response(self, data):
        return Response({"data": data, "page": self.page.number, "total": self.page.paginator.count})


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
            cache.set("h", "ok", 5)
            redis_ok = cache.get("h") == "ok"
        except Exception:
            redis_ok = False
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "version": "1.0.0"}, status=code)


class AccountCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Accounts"], summary="Creer un wallet")
    def post(self, request):
        d = request.data
        acc = Account.objects.create(
            account_type=d.get("account_type", "user"), owner_type=d.get("owner_type", "user"),
            owner_id=d.get("owner_id") or getattr(request.user, "auth_user_id", None),
            currency=d.get("currency", "XAF"), label=d.get("label"))
        return Response({"id": str(acc.id), "account_type": acc.account_type, "currency": acc.currency,
                         "balance": 0, "message": "Account created"}, status=status.HTTP_201_CREATED)


class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Accounts"], summary="Detail compte + solde disponible")
    def get(self, request, account_id):
        try:
            acc = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return Response({"detail": "Compte introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": str(acc.id), "account_type": acc.account_type,
                         "owner_id": str(acc.owner_id) if acc.owner_id else None,
                         "currency": acc.currency, "balance": float(acc.balance),
                         "hold_amount": float(acc.hold_amount),
                         "available_balance": float(acc.available_balance),
                         "status": acc.status, "label": acc.label})


class AccountByOwnerView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Accounts"], summary="Trouver wallets par owner")
    def get(self, request, owner_id):
        accs = Account.objects.filter(owner_id=owner_id)
        data = [{"id": str(a.id), "account_type": a.account_type, "currency": a.currency,
                 "balance": float(a.balance), "available_balance": float(a.available_balance)} for a in accs]
        return Response({"data": data})


class AccountFreezeView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Accounts"], summary="Geler un wallet")
    def post(self, request, account_id):
        try:
            acc = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return Response({"detail": "Introuvable."}, status=status.HTTP_404_NOT_FOUND)
        acc.status = AccountStatus.FROZEN
        acc.save(update_fields=["status", "updated_at"])
        return Response({"message": "Account frozen"})


class AccountUnfreezeView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Accounts"], summary="Degeler un wallet")
    def post(self, request, account_id):
        try:
            acc = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return Response({"detail": "Introuvable."}, status=status.HTTP_404_NOT_FOUND)
        acc.status = AccountStatus.ACTIVE
        acc.save(update_fields=["status", "updated_at"])
        return Response({"message": "Account unfrozen"})


class CreditView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Ledger"], summary="Crediter un compte (double-entry)", request=CreditSerializer)
    def post(self, request):
        serializer = CreditSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        d = serializer.validated_data
        ltx, err = LedgerService.credit(
            d["account_id"], d["amount"], d["currency"],
            d.get("platform_id"), d.get("source", "payment"),
            d.get("source_reference_id"), d["idempotency_key"],
            d.get("description"))
        if err == "idempotent_hit":
            return Response({"transaction_id": str(ltx.id), "message": "Idempotent hit"})
        if err:
            codes = {"account_not_found": 404, "account_frozen": 409}
            return Response({"detail": err}, status=codes.get(err, 400))
        acc = Account.objects.get(id=d["account_id"])
        return Response({"transaction_id": str(ltx.id), "new_balance": float(acc.balance),
                        "message": "Credit completed"}, status=status.HTTP_201_CREATED)

class DebitView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Ledger"], summary="Debiter un compte (double-entry)", request=DebitSerializer)
    def post(self, request):
        serializer = DebitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        d = serializer.validated_data
        ltx, err = LedgerService.debit(
            d.get("account_id"), d.get("amount"), d.get("currency", "XAF"),
            d.get("platform_id"), d.get("source", "platform"),
            d.get("source_reference_id"), d.get("idempotency_key"), d.get("description"))
        if err == "idempotent_hit":
            return Response({"transaction_id": str(ltx.id), "message": "Idempotent hit"})
        if err:
            codes = {"account_not_found": 404, "account_frozen": 409, "insufficient_balance": 403}
            return Response({"detail": err}, status=codes.get(err, 400))
        acc = Account.objects.get(id=d["account_id"])
        return Response({"transaction_id": str(ltx.id), "new_balance": float(acc.balance),
                         "message": "Debit completed"}, status=status.HTTP_201_CREATED)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Ledger"], summary="Virement entre comptes", request=TransferSerializer)
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        d = serializer.validated_data
        ltx, err = LedgerService.transfer(
            d["from_account_id"], d["to_account_id"], d["amount"],
            d.get("currency", "XAF"), d.get("platform_id"),
            d.get("idempotency_key"), d.get("description"))
        if err == "idempotent_hit":
            return Response({"transaction_id": str(ltx.id), "message": "Idempotent hit"})
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"transaction_id": str(ltx.id), "message": "Transfer completed"}, status=status.HTTP_201_CREATED)


class SplitView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Ledger"], summary="Split (partage commission)", request=SplitSerializer)
    def post(self, request):
        serializer = SplitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        d = serializer.validated_data
        ltx, err = LedgerService.split(
            d["source_account_id"], d["amount"], d.get("currency", "XAF"),
            d.get("platform_id"), d.get("targets", []),
            d.get("idempotency_key"), d.get("source_reference_id"), d.get("description"))
        if err == "idempotent_hit":
            return Response({"transaction_id": str(ltx.id), "message": "Idempotent hit"})
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        entries = LedgerEntry.objects.filter(transaction=ltx)
        data = [{"account_id": str(e.account_id), "direction": e.direction, "amount": float(e.amount)} for e in entries]
        return Response({"transaction_id": str(ltx.id), "entries": data, "message": "Split completed"}, status=status.HTTP_201_CREATED)


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Ledger"], summary="Historique mouvements")
    def get(self, request, account_id):
        entries = LedgerEntry.objects.filter(account_id=account_id).select_related("transaction")
        paginator = Paginator()
        page = paginator.paginate_queryset(entries, request)
        data = [{"transaction_id": str(e.transaction_id), "type": e.transaction.transaction_type,
                 "direction": e.direction, "amount": float(e.amount), "balance_after": float(e.balance_after),
                 "description": e.transaction.description, "created_at": e.created_at.isoformat()} for e in page]
        return paginator.get_paginated_response(data)


class HoldCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Holds"], summary="Creer un hold", request=HoldSerializer)
    def post(self, request):
        serializer = HoldSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        d = serializer.validated_data
        hold, err = LedgerService.create_hold(
            d.get("account_id"), d.get("amount"), d.get("reason"),
            d.get("idempotency_key"), d.get("ttl_seconds", 3600), d.get("source_reference_id"))
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"hold_id": str(hold.id), "amount": float(hold.amount),
                         "expires_at": hold.expires_at.isoformat()}, status=status.HTTP_201_CREATED)


class HoldCaptureView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Holds"], summary="Capturer un hold")
    def post(self, request, hold_id):
        hold, err = LedgerService.capture_hold(hold_id, request.data.get("capture_amount"))
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"hold_id": str(hold.id), "status": "captured"})


class HoldReleaseView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Holds"], summary="Liberer un hold")
    def post(self, request, hold_id):
        hold, err = LedgerService.release_hold(hold_id)
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"hold_id": str(hold.id), "status": "released"})


class SplitRuleListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Split Rules"], summary="CRUD regles de split")
    def post(self, request):
        d = request.data
        rule = SplitRule.objects.create(platform_id=d["platform_id"], name=d["name"], rules=d["rules"])
        return Response({"id": str(rule.id), "name": rule.name}, status=status.HTTP_201_CREATED)
    def get(self, request):
        qs = SplitRule.objects.filter(is_active=True)
        pid = request.GET.get("platform_id")
        if pid:
            qs = qs.filter(platform_id=pid)
        return Response({"data": [{"id": str(r.id), "name": r.name, "rules": r.rules} for r in qs]})


class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Admin"], summary="Stats globales")
    def get(self, request):
        from django.db.models import Sum
        total = Account.objects.filter(account_type="user").aggregate(s=Sum("balance"))["s"] or 0
        return Response({"total_accounts": Account.objects.count(), "total_user_balance": float(total)})


class AdminAuditView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Admin"], summary="Audit equilibre ledger")
    def post(self, request):
        return Response(LedgerService.verify_integrity())


class AdminAdjustmentView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Admin"], summary="Ajustement correctif")
    def post(self, request):
        d = request.data
        if not d.get("amount") or not d.get("account_id"):
            return Response({"detail": "account_id et amount obligatoires."}, status=status.HTTP_400_BAD_REQUEST)
        direction = d.get("direction")
        if direction not in ("credit", "debit"):
            return Response({"detail": "direction doit etre 'credit' ou 'debit'."}, status=status.HTTP_400_BAD_REQUEST)
        if not d.get("reason"):
            return Response({"detail": "reason obligatoire."}, status=status.HTTP_400_BAD_REQUEST)
        pid = d.get("platform_id", "00000000-0000-0000-0000-000000000000")
        if direction == "credit":
            ltx, err = LedgerService.credit(d["account_id"], d["amount"], d.get("currency", "XAF"),
                                              pid, "admin", None, d.get("idempotency_key"), d["reason"])
        else:
            ltx, err = LedgerService.debit(d["account_id"], d["amount"], d.get("currency", "XAF"),
                                             pid, "admin", None, d.get("idempotency_key"), d["reason"])
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"transaction_id": str(ltx.id), "message": f"Adjustment {direction} completed"}, status=status.HTTP_201_CREATED)
