# AGT Payment Service - CDC v1.0

> Version : 1.0 | Statut : Implementation-ready

## Perimetre
Execution transactions externes. Multi-provider: Orange Money, MTN MoMo, Stripe, PayPal.
Ne contient PAS de logique metier. Recoit un montant, une devise, un provider, execute.

## Tables (6)
transactions, transaction_status_history, webhook_logs, provider_configs, platform_payment_config, reconciliation_reports (future).

## Machine a etats
pending -> processing -> succeeded/failed/expired
pending -> succeeded/failed/expired/cancelled

Etats terminaux: succeeded, failed, expired, cancelled. Aucune transition sortante.

## Providers (Strategy Pattern)
Chaque provider = un adapter avec: initiate_payment(), normalize_webhook(), normalize_status().

## Securite webhooks
Signature HMAC + IP whitelist + replay protection (Redis 72h) + timestamp validation.

## Idempotency
idempotency_key UNIQUE NOT NULL. Meme cle = retour transaction existante.

## Port : 7005
