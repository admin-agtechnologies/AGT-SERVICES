# AGT Subscription Service - CDC v1.0

> Version : 1.0 | Statut : Implementation-ready

## Perimetre
Plans, abonnements, quotas temps reel, prorata, trial, grace, organisations B2B.

## Tables (10)
plans, plan_prices, plan_quotas, subscriptions, subscription_quotas_usage, quota_reservations, subscription_events, organizations, organization_members, platform_subscription_config.

## Cycle de vie
pending_payment > active > cancelled/expired/suspended
trial > active (si paiement) | downgrade/suspend/expire (selon config)

## Quotas
- check < 50ms (cache Redis)
- reserve/confirm/release (atomique)
- hard limit ou overage
- reset periodique au renouvellement

## Port : 7004
