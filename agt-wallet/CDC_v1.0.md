# AGT Wallet Service - CDC v1.0

> Ledger double-entry centralise. Append-only. Aucune modification/suppression d'ecriture.

## Principes
1. Chaque mouvement = 1 debit + 1 credit equilibres
2. Append-only : corrections par ecriture inverse (reversal)
3. balance = cache. Solde reel = sum(credits) - sum(debits)
4. Transactions atomiques PostgreSQL (SELECT FOR UPDATE)
5. Idempotency_key UNIQUE sur chaque operation

## Types de comptes
user, organization, platform_system, escrow, external

## Operations
credit, debit, transfer, split, hold/capture/release, adjustment, reversal

## Tables (6)
accounts, ledger_transactions, ledger_entries, holds, cashout_requests, split_rules

## Port : 7006
