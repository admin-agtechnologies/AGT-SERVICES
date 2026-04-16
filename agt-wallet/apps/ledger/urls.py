from django.urls import path
from apps.ledger.views import (
    HealthCheckView, AccountCreateView, AccountDetailView, AccountByOwnerView,
    AccountFreezeView, AccountUnfreezeView, CreditView, DebitView, TransferView,
    SplitView, TransactionHistoryView, HoldCreateView, HoldCaptureView, HoldReleaseView,
    HoldDetailView, HoldListView, SplitRuleListCreateView, AdminStatsView,
    AdminAuditView, AdminAdjustmentView,
)

urlpatterns = [
    path("wallet/health", HealthCheckView.as_view()),
    path("wallet/accounts", AccountCreateView.as_view()),
    path("wallet/accounts/<uuid:account_id>", AccountDetailView.as_view()),
    path("wallet/accounts/by-owner/<uuid:owner_id>", AccountByOwnerView.as_view()),
    path("wallet/accounts/<uuid:account_id>/freeze", AccountFreezeView.as_view()),
    path("wallet/accounts/<uuid:account_id>/unfreeze", AccountUnfreezeView.as_view()),
    path("wallet/accounts/<uuid:account_id>/transactions", TransactionHistoryView.as_view()),
    path("wallet/credit", CreditView.as_view()),
    path("wallet/debit", DebitView.as_view()),
    path("wallet/transfer", TransferView.as_view()),
    path("wallet/split", SplitView.as_view()),
    path("wallet/holds", HoldListView.as_view()),
    path("wallet/holds/create", HoldCreateView.as_view()),
    path("wallet/holds/<uuid:hold_id>", HoldDetailView.as_view()),
    path("wallet/holds/<uuid:hold_id>/capture", HoldCaptureView.as_view()),
    path("wallet/holds/<uuid:hold_id>/release", HoldReleaseView.as_view()),
    path("wallet/split-rules", SplitRuleListCreateView.as_view()),
    path("wallet/admin/stats", AdminStatsView.as_view()),
    path("wallet/admin/audit-ledger", AdminAuditView.as_view()),
    path("wallet/admin/adjustment", AdminAdjustmentView.as_view()),
]

