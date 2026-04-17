# ============================================================
# AGT Subscription Service - Fix Script (PowerShell)
# A executer a la racine de agt-subscription/
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "AGT Subscription - application des fixes..." -ForegroundColor Cyan
Write-Host ""

# ──────────────────────────────────────────────────────────────
# B1 - DELETE member : retourner 204 au lieu de 200
# ──────────────────────────────────────────────────────────────
Write-Host "[B1] Fix DELETE member -> status 204..." -ForegroundColor Yellow

$viewsPath = "apps\subscriptions\views.py"
$content = Get-Content $viewsPath -Raw -Encoding UTF8

$old1 = 'return Response({"message": "Member removed"})'
$new1 = 'return Response(status=status.HTTP_204_NO_CONTENT)'

if ($content.Contains($old1)) {
    $content = $content.Replace($old1, $new1)
    [System.IO.File]::WriteAllText((Resolve-Path $viewsPath).Path, $content, [System.Text.Encoding]::UTF8)
    Write-Host "     OK" -ForegroundColor Green
} else {
    Write-Host "     ATTENTION : pattern non trouve - verifier manuellement" -ForegroundColor Red
}

# ──────────────────────────────────────────────────────────────
# B2 - QuotaCheckView : accepter "amount" ET "requested"
# ──────────────────────────────────────────────────────────────
Write-Host "[B2] Fix QuotaCheckView -> accepter 'amount' en plus de 'requested'..." -ForegroundColor Yellow

$content = Get-Content $viewsPath -Raw -Encoding UTF8
$old2 = 'd.get("subscriber_id"), d.get("quota_key"), d.get("requested", 1))'
$new2 = 'd.get("subscriber_id"), d.get("quota_key"),' + "`n" + '                                     d.get("amount") or d.get("requested", 1))'

if ($content.Contains($old2)) {
    $content = $content.Replace($old2, $new2)
    [System.IO.File]::WriteAllText((Resolve-Path $viewsPath).Path, $content, [System.Text.Encoding]::UTF8)
    Write-Host "     OK" -ForegroundColor Green
} else {
    Write-Host "     ATTENTION : pattern non trouve - verifier manuellement" -ForegroundColor Red
}

# ──────────────────────────────────────────────────────────────
# B3 - tests/test_all.py : reserve retourne 201 pas 200
# ──────────────────────────────────────────────────────────────
Write-Host "[B3] Fix tests/test_all.py -> reserve status 201..." -ForegroundColor Yellow

$testsPath = "tests\test_all.py"
$content = Get-Content $testsPath -Raw -Encoding UTF8

# Strategie simple : on compte les occurrences avant
$countBefore = ([regex]::Matches($content, 'quotas/reserve')).Count
$fixed = 0

# Remplace chaque bloc reserve + assertEqual 200 par 201
# On boucle pour attraper les deux occurrences (confirm + release)
$pattern = '(\/quotas\/reserve[\s\S]{1,150}?)self\.assertEqual\(resp\.status_code, 200\)'
$matches = [regex]::Matches($content, $pattern)

foreach ($m in $matches) {
    $oldBlock = $m.Value
    $newBlock = $oldBlock -replace 'self\.assertEqual\(resp\.status_code, 200\)', 'self.assertEqual(resp.status_code, 201)'
    $content = $content.Replace($oldBlock, $newBlock)
    $fixed++
}

if ($fixed -gt 0) {
    [System.IO.File]::WriteAllText((Resolve-Path $testsPath).Path, $content, [System.Text.Encoding]::UTF8)
    Write-Host "     OK ($fixed occurrence(s) corrigee(s))" -ForegroundColor Green
} else {
    Write-Host "     ATTENTION : pattern non trouve - verifier manuellement" -ForegroundColor Red
    Write-Host "     => Dans tests/test_all.py, remplacer les 2x assertEqual(status_code, 200) apres /quotas/reserve par 201" -ForegroundColor Yellow
}

# ──────────────────────────────────────────────────────────────
# B4 - pytest.ini
# ──────────────────────────────────────────────────────────────
Write-Host "[B4] Fix pytest.ini -> testpaths=tests, settings_test..." -ForegroundColor Yellow

$pytestLines = @(
    "[pytest]",
    "DJANGO_SETTINGS_MODULE = config.settings_test",
    "python_files = test_*.py",
    "python_classes = Test*",
    "python_functions = test_*",
    "testpaths = tests",
    "addopts = -v --tb=short",
    ""
)
$pytestContent = $pytestLines -join "`r`n"
[System.IO.File]::WriteAllText((Join-Path (Get-Location).Path "pytest.ini"), $pytestContent, [System.Text.Encoding]::UTF8)
Write-Host "     OK" -ForegroundColor Green

# ──────────────────────────────────────────────────────────────
# B5 - docker-compose.yml : ajouter agt_network
# Les hostnames db/redis sont corriges en agt-sub-db/agt-sub-redis
# ──────────────────────────────────────────────────────────────
Write-Host "[B5] Fix docker-compose.yml -> ajout agt_network..." -ForegroundColor Yellow

$dockerLines = @(
    "services:",
    "  db:",
    "    image: postgres:15-alpine",
    "    container_name: agt-sub-db",
    "    restart: unless-stopped",
    "    environment:",
    "      POSTGRES_DB: agt_subscription_db",
    "      POSTGRES_USER: sub_user",
    "      POSTGRES_PASSWORD: sub_password",
    "    volumes:",
    "      - postgres_data:/var/lib/postgresql/data",
    "    ports:",
    '      - "5435:5432"',
    "    healthcheck:",
    '      test: ["CMD-SHELL", "pg_isready -U sub_user -d agt_subscription_db"]',
    "      interval: 10s",
    "      timeout: 5s",
    "      retries: 5",
    "    networks:",
    "      - agt_network",
    "",
    "  redis:",
    "    image: redis:7-alpine",
    "    container_name: agt-sub-redis",
    "    restart: unless-stopped",
    "    volumes:",
    "      - redis_data:/data",
    "    ports:",
    '      - "6382:6379"',
    "    healthcheck:",
    '      test: ["CMD", "redis-cli", "ping"]',
    "      interval: 10s",
    "      timeout: 5s",
    "      retries: 5",
    "    networks:",
    "      - agt_network",
    "",
    "  subscription:",
    "    build:",
    "      context: .",
    "      target: production",
    "    container_name: agt-sub-service",
    "    restart: unless-stopped",
    "    env_file:",
    "      - .env",
    "    environment:",
    "      DATABASE_URL: postgresql://sub_user:sub_password@agt-sub-db:5432/agt_subscription_db",
    "      REDIS_URL: redis://agt-sub-redis:6379/4",
    "      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem",
    "    volumes:",
    "      - ./keys:/app/keys:ro",
    "    ports:",
    '      - "7004:7004"',
    "    depends_on:",
    "      db:",
    "        condition: service_healthy",
    "      redis:",
    "        condition: service_healthy",
    "    healthcheck:",
    '      test: ["CMD-SHELL", "curl -f http://localhost:7004/api/v1/subscriptions/health || exit 1"]',
    "      interval: 30s",
    "      timeout: 10s",
    "      retries: 3",
    "      start_period: 40s",
    "    networks:",
    "      - agt_network",
    "",
    "  subscription-dev:",
    "    build:",
    "      context: .",
    "      target: builder",
    "    container_name: agt-sub-dev",
    "    restart: unless-stopped",
    '    command: sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:7004"',
    "    env_file:",
    "      - .env",
    "    environment:",
    "      DATABASE_URL: postgresql://sub_user:sub_password@agt-sub-db:5432/agt_subscription_db",
    "      REDIS_URL: redis://agt-sub-redis:6379/4",
    '      DEBUG: "True"',
    "      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem",
    "    volumes:",
    "      - .:/app",
    "      - ./keys:/app/keys:ro",
    "    ports:",
    '      - "7004:7004"',
    "    depends_on:",
    "      db:",
    "        condition: service_healthy",
    "      redis:",
    "        condition: service_healthy",
    "    profiles:",
    "      - dev",
    "    networks:",
    "      - agt_network",
    "",
    "volumes:",
    "  postgres_data:",
    "  redis_data:",
    "",
    "networks:",
    "  agt_network:",
    "    external: true",
    ""
)
$dockerContent = $dockerLines -join "`r`n"
[System.IO.File]::WriteAllText((Join-Path (Get-Location).Path "docker-compose.yml"), $dockerContent, [System.Text.Encoding]::UTF8)
Write-Host "     OK" -ForegroundColor Green

# ──────────────────────────────────────────────────────────────
# Resume
# ──────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Fixes appliques avec succes !" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines etapes :" -ForegroundColor White
Write-Host "  1. Copier auth_public.pem dans keys/" -ForegroundColor Gray
Write-Host "  2. Copier .env.example en .env et remplir S2S_CLIENT_ID/SECRET" -ForegroundColor Gray
Write-Host "  3. docker compose up -d --build" -ForegroundColor Gray
Write-Host "  4. docker compose exec subscription python manage.py migrate" -ForegroundColor Gray
Write-Host "  5. docker compose exec subscription python -m pytest -v" -ForegroundColor Gray
Write-Host ""