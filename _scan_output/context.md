# AGT CONTEXT

## PROJECT TREE
`	ext
\agt-auth
\agt-chatbot
\agt-notification
\agt-payment
\agt-search
\agt-subscription
\agt-users
\agt-wallet
\docs
\next
\_scan_output
\Docker compose.infra.yml
\nginx.conf
\notes.md
\README.md
\scanner.ps1
\standards.md
\todo.md
\agt-auth\apps
\agt-auth\common
\agt-auth\config
\agt-auth\keys
\agt-auth\scripts
\agt-auth\.env
\agt-auth\.env.example
\agt-auth\CDC_v1.0.md
\agt-auth\docker-compose.yml
\agt-auth\Dockerfile
\agt-auth\manage.py
\agt-auth\pytest.ini
\agt-auth\README.md
\agt-auth\requirements.txt
\agt-auth\apps\authentication
\agt-auth\apps\platforms
\agt-auth\apps\__init__.py
\agt-auth\apps\authentication\management
\agt-auth\apps\authentication\tests
\agt-auth\apps\authentication\authentication.py
\agt-auth\apps\authentication\exceptions.py
\agt-auth\apps\authentication\models.py
\agt-auth\apps\authentication\pagination.py
\agt-auth\apps\authentication\permissions.py
\agt-auth\apps\authentication\serializers.py
\agt-auth\apps\authentication\services.py
\agt-auth\apps\authentication\swagger.py
\agt-auth\apps\authentication\urls.py
\agt-auth\apps\authentication\utils.py
\agt-auth\apps\authentication\views_admin.py
\agt-auth\apps\authentication\views_auth.py
\agt-auth\apps\authentication\views_sessions.py
\agt-auth\apps\authentication\__init__.py
\agt-auth\apps\authentication\management\commands
\agt-auth\apps\authentication\management\__init__.py
\agt-auth\apps\authentication\management\commands\cleanup_expired.py
\agt-auth\apps\authentication\management\commands\generate_keys.py
\agt-auth\apps\authentication\management\commands\__init__.py
\agt-auth\apps\authentication\tests\test_all.py
\agt-auth\apps\authentication\tests\__init__.py
\agt-auth\apps\platforms\serializers.py
\agt-auth\apps\platforms\urls.py
\agt-auth\apps\platforms\views.py
\agt-auth\apps\platforms\__init__.py
\agt-auth\common\middleware.py
\agt-auth\common\__init__.py
\agt-auth\config\settings.py
\agt-auth\config\settings_test.py
\agt-auth\config\urls.py
\agt-auth\config\wsgi.py
\agt-auth\config\__init__.py
\agt-auth\keys\private.pem
\agt-auth\keys\public.pem
\agt-auth\scripts\setup.ps1
\agt-auth\scripts\setup.sh
\agt-chatbot\apps
\agt-chatbot\common
\agt-chatbot\config
\agt-chatbot\keys
\agt-chatbot\scripts
\agt-chatbot\.env.example
\agt-chatbot\CDC_v1.0.md
\agt-chatbot\docker-compose.yml
\agt-chatbot\Dockerfile
\agt-chatbot\manage.py
\agt-chatbot\pytest.ini
\agt-chatbot\README.md
\agt-chatbot\requirements.txt
\agt-chatbot\apps\ai_providers
\agt-chatbot\apps\bots
\agt-chatbot\apps\conversations
\agt-chatbot\apps\knowledge
\agt-chatbot\apps\__init__.py
\agt-chatbot\apps\ai_providers\__init__.py
\agt-chatbot\apps\bots\models.py
\agt-chatbot\apps\bots\__init__.py
\agt-chatbot\apps\conversations\tests
\agt-chatbot\apps\conversations\orchestrator.py
\agt-chatbot\apps\conversations\urls.py
\agt-chatbot\apps\conversations\views.py
\agt-chatbot\apps\conversations\__init__.py
\agt-chatbot\apps\conversations\tests\test_all.py
\agt-chatbot\apps\conversations\tests\__init__.py
\agt-chatbot\apps\knowledge\__init__.py
\agt-chatbot\common\authentication.py
\agt-chatbot\common\__init__.py
\agt-chatbot\config\settings.py
\agt-chatbot\config\settings_test.py
\agt-chatbot\config\urls.py
\agt-chatbot\config\wsgi.py
\agt-chatbot\config\__init__.py
\agt-chatbot\scripts\setup.ps1
\agt-chatbot\scripts\setup.sh
\agt-notification\apps
\agt-notification\common
\agt-notification\config
\agt-notification\keys
\agt-notification\providers
\agt-notification\scripts
\agt-notification\workers
\agt-notification\.env
\agt-notification\.env.example
\agt-notification\CDC_v1.0.md
\agt-notification\docker-compose.yml
\agt-notification\Dockerfile
\agt-notification\manage.py
\agt-notification\pytest.ini
\agt-notification\README.md
\agt-notification\requirements.txt
\agt-notification\apps\campaigns
\agt-notification\apps\devices
\agt-notification\apps\notifications
\agt-notification\apps\templates_mgr
\agt-notification\apps\__init__.py
\agt-notification\apps\campaigns\models.py
\agt-notification\apps\campaigns\urls.py
\agt-notification\apps\campaigns\views.py
\agt-notification\apps\campaigns\__init__.py
\agt-notification\apps\devices\models.py
\agt-notification\apps\devices\urls.py
\agt-notification\apps\devices\views.py
\agt-notification\apps\devices\__init__.py
\agt-notification\apps\notifications\tests
\agt-notification\apps\notifications\authentication.py
\agt-notification\apps\notifications\exceptions.py
\agt-notification\apps\notifications\models.py
\agt-notification\apps\notifications\pagination.py
\agt-notification\apps\notifications\services.py
\agt-notification\apps\notifications\urls.py
\agt-notification\apps\notifications\views.py
\agt-notification\apps\notifications\__init__.py
\agt-notification\apps\notifications\tests\test_all.py
\agt-notification\apps\notifications\tests\__init__.py
\agt-notification\apps\templates_mgr\models.py
\agt-notification\apps\templates_mgr\urls.py
\agt-notification\apps\templates_mgr\views.py
\agt-notification\apps\templates_mgr\__init__.py
\agt-notification\common\__init__.py
\agt-notification\config\celery.py
\agt-notification\config\settings.py
\agt-notification\config\settings_test.py
\agt-notification\config\urls.py
\agt-notification\config\wsgi.py
\agt-notification\config\__init__.py
\agt-notification\keys\auth_public.pem
\agt-notification\providers\providers.py
\agt-notification\providers\__init__.py
\agt-notification\scripts\setup.ps1
\agt-notification\scripts\setup.sh
\agt-notification\workers\tasks.py
\agt-notification\workers\__init__.py
\agt-payment\apps
\agt-payment\common
\agt-payment\config
\agt-payment\keys
\agt-payment\scripts
\agt-payment\.env
\agt-payment\.env.example
\agt-payment\CDC_v1.0.md
\agt-payment\docker-compose.yml
\agt-payment\Dockerfile
\agt-payment\manage.py
\agt-payment\pytest.ini
\agt-payment\README.md
\agt-payment\requirements.txt
\agt-payment\apps\payments
\agt-payment\apps\providers
\agt-payment\apps\webhooks
\agt-payment\apps\__init__.py
\agt-payment\apps\payments\tests
\agt-payment\apps\payments\models.py
\agt-payment\apps\payments\service.py
\agt-payment\apps\payments\urls.py
\agt-payment\apps\payments\views.py
\agt-payment\apps\payments\__init__.py
\agt-payment\apps\payments\tests\test_all.py
\agt-payment\apps\payments\tests\__init__.py
\agt-payment\apps\providers\adapters.py
\agt-payment\apps\providers\__init__.py
\agt-payment\apps\webhooks\__init__.py
\agt-payment\common\authentication.py
\agt-payment\common\__init__.py
\agt-payment\config\settings.py
\agt-payment\config\settings_test.py
\agt-payment\config\urls.py
\agt-payment\config\wsgi.py
\agt-payment\config\__init__.py
\agt-payment\keys\auth_public.pem
\agt-payment\scripts\setup.ps1
\agt-payment\scripts\setup.sh
\agt-search\apps
\agt-search\common
\agt-search\config
\agt-search\keys
\agt-search\scripts
\agt-search\.env
\agt-search\.env.example
\agt-search\CDC_v1.0.md
\agt-search\docker-compose.yml
\agt-search\Dockerfile
\agt-search\manage.py
\agt-search\pytest.ini
\agt-search\README.md
\agt-search\requirements.txt
\agt-search\apps\indexes
\agt-search\apps\search
\agt-search\apps\__init__.py
\agt-search\apps\indexes\models.py
\agt-search\apps\indexes\__init__.py
\agt-search\apps\search\tests
\agt-search\apps\search\es_service.py
\agt-search\apps\search\urls.py
\agt-search\apps\search\views.py
\agt-search\apps\search\__init__.py
\agt-search\apps\search\tests\test_all.py
\agt-search\apps\search\tests\__init__.py
\agt-search\common\authentication.py
\agt-search\common\__init__.py
\agt-search\config\settings.py
\agt-search\config\settings_test.py
\agt-search\config\urls.py
\agt-search\config\wsgi.py
\agt-search\config\__init__.py
\agt-search\keys\auth_public.pem
\agt-search\scripts\setup.ps1
\agt-search\scripts\setup.sh
\agt-subscription\apps
\agt-subscription\common
\agt-subscription\config
\agt-subscription\keys
\agt-subscription\scripts
\agt-subscription\.env
\agt-subscription\.env.example
\agt-subscription\CDC_v1.0.md
\agt-subscription\docker-compose.yml
\agt-subscription\Dockerfile
\agt-subscription\manage.py
\agt-subscription\pytest.ini
\agt-subscription\README.md
\agt-subscription\requirements.txt
\agt-subscription\apps\organizations
\agt-subscription\apps\plans
\agt-subscription\apps\quotas
\agt-subscription\apps\subscriptions
\agt-subscription\apps\__init__.py
\agt-subscription\apps\organizations\models.py
\agt-subscription\apps\organizations\__init__.py
\agt-subscription\apps\plans\models.py
\agt-subscription\apps\plans\__init__.py
\agt-subscription\apps\quotas\service.py
\agt-subscription\apps\quotas\__init__.py
\agt-subscription\apps\subscriptions\tests
\agt-subscription\apps\subscriptions\models.py
\agt-subscription\apps\subscriptions\service.py
\agt-subscription\apps\subscriptions\urls.py
\agt-subscription\apps\subscriptions\views.py
\agt-subscription\apps\subscriptions\__init__.py
\agt-subscription\apps\subscriptions\tests\test_all.py
\agt-subscription\apps\subscriptions\tests\__init__.py
\agt-subscription\common\authentication.py
\agt-subscription\common\__init__.py
\agt-subscription\config\settings.py
\agt-subscription\config\settings_test.py
\agt-subscription\config\urls.py
\agt-subscription\config\wsgi.py
\agt-subscription\config\__init__.py
\agt-subscription\keys\auth_public.pem
\agt-subscription\scripts\setup.ps1
\agt-subscription\scripts\setup.sh
\agt-users\apps
\agt-users\common
\agt-users\config
\agt-users\keys
\agt-users\scripts
\agt-users\.env
\agt-users\.env.example
\agt-users\CDC_v1.0.md
\agt-users\docker-compose.yml
\agt-users\Dockerfile
\agt-users\manage.py
\agt-users\pytest.ini
\agt-users\README.md
\agt-users\requirements.txt
\agt-users\apps\documents
\agt-users\apps\roles
\agt-users\apps\users
\agt-users\apps\__init__.py
\agt-users\apps\documents\models.py
\agt-users\apps\documents\urls.py
\agt-users\apps\documents\views.py
\agt-users\apps\documents\__init__.py
\agt-users\apps\roles\models.py
\agt-users\apps\roles\urls.py
\agt-users\apps\roles\views.py
\agt-users\apps\roles\__init__.py
\agt-users\apps\users\tests
\agt-users\apps\users\authentication.py
\agt-users\apps\users\exceptions.py
\agt-users\apps\users\models.py
\agt-users\apps\users\pagination.py
\agt-users\apps\users\serializers.py
\agt-users\apps\users\services.py
\agt-users\apps\users\urls.py
\agt-users\apps\users\views.py
\agt-users\apps\users\__init__.py
\agt-users\apps\users\tests\test_all.py
\agt-users\apps\users\tests\__init__.py
\agt-users\common\middleware.py
\agt-users\common\__init__.py
\agt-users\config\settings.py
\agt-users\config\settings_test.py
\agt-users\config\urls.py
\agt-users\config\wsgi.py
\agt-users\config\__init__.py
\agt-users\keys\auth_public.pem
\agt-users\scripts\setup.ps1
\agt-users\scripts\setup.sh
\agt-wallet\apps
\agt-wallet\common
\agt-wallet\config
\agt-wallet\keys
\agt-wallet\scripts
\agt-wallet\.env
\agt-wallet\.env.example
\agt-wallet\CDC_v1.0.md
\agt-wallet\docker-compose.yml
\agt-wallet\Dockerfile
\agt-wallet\manage.py
\agt-wallet\pytest.ini
\agt-wallet\README.md
\agt-wallet\requirements.txt
\agt-wallet\apps\accounts
\agt-wallet\apps\cashout
\agt-wallet\apps\holds
\agt-wallet\apps\ledger
\agt-wallet\apps\__init__.py
\agt-wallet\apps\accounts\models.py
\agt-wallet\apps\accounts\__init__.py
\agt-wallet\apps\cashout\__init__.py
\agt-wallet\apps\holds\__init__.py
\agt-wallet\apps\ledger\tests
\agt-wallet\apps\ledger\service.py
\agt-wallet\apps\ledger\urls.py
\agt-wallet\apps\ledger\views.py
\agt-wallet\apps\ledger\__init__.py
\agt-wallet\apps\ledger\tests\test_all.py
\agt-wallet\apps\ledger\tests\__init__.py
\agt-wallet\common\authentication.py
\agt-wallet\common\__init__.py
\agt-wallet\config\settings.py
\agt-wallet\config\settings_test.py
\agt-wallet\config\urls.py
\agt-wallet\config\wsgi.py
\agt-wallet\config\__init__.py
\agt-wallet\keys\auth_public.pem
\agt-wallet\scripts\setup.ps1
\agt-wallet\scripts\setup.sh
\docs\GETTING_STARTED.md
\docs\GUIDE_AUTH.md
\docs\GUIDE_NOTIFICATION.md
\docs\GUIDE_SUBSCRIPTION.md
\docs\GUIDE_USERS.md
\next\prompt_fisrt_task.md
\next\prompt_initialisation.md
\next\prompt_todo.md

`

## FILES
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\Docker compose.infra.yml (2.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\nginx.conf (10.55 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\notes.md (2.47 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\README.md (10.49 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\standards.md (11.65 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\todo.md (15.57 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\.env (3.52 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\.env.example (3.52 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\CDC_v1.0.md (3.63 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\docker-compose.yml (2.99 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\Dockerfile (0.81 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\manage.py (0.48 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\README.md (4.99 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\requirements.txt (0.67 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\authentication.py (3.08 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\exceptions.py (0.88 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\models.py (9.44 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\pagination.py (0.47 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\permissions.py (0.63 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\serializers.py (4.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\services.py (9.57 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\swagger.py (7.53 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\urls.py (4.07 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\utils.py (1.6 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\views_admin.py (16.12 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\views_auth.py (17.26 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\views_sessions.py (16.41 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\commands\cleanup_expired.py (1.05 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\commands\generate_keys.py (1.51 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\commands\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\tests\test_all.py (11.4 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\serializers.py (1.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\urls.py (0.31 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\views.py (2.83 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\common\middleware.py (3.47 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\settings.py (9.69 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\settings_test.py (1.21 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\urls.py (0.54 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\.env.example (0.28 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\CDC_v1.0.md (0.62 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\docker-compose.yml (2.07 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\Dockerfile (0.52 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\manage.py (0.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\README.md (0.9 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\requirements.txt (0.3 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\ai_providers\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\bots\models.py (8.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\bots\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\orchestrator.py (7.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\urls.py (1.06 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\views.py (11.42 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\tests\test_all.py (3.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\knowledge\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\common\authentication.py (1.35 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\settings.py (2.57 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\settings_test.py (0.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\urls.py (0.46 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\.env (1.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\.env.example (1.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\CDC_v1.0.md (2.6 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\docker-compose.yml (4.28 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\Dockerfile (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\manage.py (0.26 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\README.md (3.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\requirements.txt (0.46 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\models.py (2.05 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\urls.py (0.54 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\views.py (4.33 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\models.py (1.08 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\urls.py (0.35 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\views.py (2.13 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\authentication.py (1.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\exceptions.py (0.53 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\models.py (6.43 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\pagination.py (0.44 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\services.py (1.68 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\urls.py (1.49 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\views.py (12.87 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\tests\test_all.py (5.74 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\models.py (3.22 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\urls.py (0.55 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\views.py (5.28 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\celery.py (0.22 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\settings.py (4.1 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\settings_test.py (1.04 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\urls.py (0.62 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\providers\providers.py (4.39 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\providers\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\workers\tasks.py (6.15 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\workers\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\.env (0.29 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\.env.example (0.29 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\CDC_v1.0.md (0.94 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\docker-compose.yml (2.11 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\Dockerfile (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\manage.py (0.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\README.md (1.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\requirements.txt (0.3 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\models.py (6.33 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\service.py (4.86 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\urls.py (1.31 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\views.py (11.29 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\tests\test_all.py (4.96 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\providers\adapters.py (3.91 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\providers\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\webhooks\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\common\authentication.py (1.44 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\settings.py (2.46 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\settings_test.py (0.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\urls.py (0.46 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\.env (0.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\.env.example (0.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\CDC_v1.0.md (0.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\docker-compose.yml (2.75 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\Dockerfile (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\manage.py (0.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\README.md (1.03 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\requirements.txt (0.31 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\indexes\models.py (3.79 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\indexes\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\es_service.py (6.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\urls.py (1.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\views.py (14.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\tests\test_all.py (1.8 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\common\authentication.py (1.35 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\settings.py (2.57 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\settings_test.py (0.71 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\urls.py (0.45 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\.env (0.41 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\.env.example (0.41 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\CDC_v1.0.md (0.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\docker-compose.yml (2.17 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\Dockerfile (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\manage.py (0.26 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\README.md (1.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\requirements.txt (0.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\organizations\models.py (1.23 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\organizations\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\plans\models.py (2.96 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\plans\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\quotas\service.py (6.04 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\quotas\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\models.py (6.06 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\service.py (5.62 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\urls.py (2.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\views.py (20.63 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\tests\test_all.py (6.28 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\common\authentication.py (1.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\settings.py (2.9 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\settings_test.py (0.72 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\urls.py (0.46 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\.env (0.98 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\.env.example (0.98 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\CDC_v1.0.md (4.21 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\docker-compose.yml (2.33 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\Dockerfile (0.48 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\manage.py (0.26 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\README.md (3.7 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\requirements.txt (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\models.py (2.21 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\urls.py (0.64 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\views.py (4.72 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\models.py (2.31 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\urls.py (1.21 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\views.py (9.9 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\authentication.py (1.92 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\exceptions.py (0.82 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\models.py (4.77 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\pagination.py (0.47 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\serializers.py (3.56 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\services.py (4.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\urls.py (1.94 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\views.py (19.81 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\tests\test_all.py (7.12 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\common\middleware.py (0.1 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\settings.py (4.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\settings_test.py (0.87 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\urls.py (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\.env (0.27 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\.env.example (0.27 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\CDC_v1.0.md (0.68 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\docker-compose.yml (2.13 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\Dockerfile (0.58 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\manage.py (0.25 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\README.md (1.29 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\requirements.txt (0.3 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\accounts\models.py (6.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\accounts\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\cashout\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\holds\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\service.py (9.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\urls.py (1.57 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\views.py (13.22 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\tests\test_all.py (5.38 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\tests\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\common\authentication.py (1.43 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\common\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\settings.py (2.47 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\settings_test.py (0.66 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\urls.py (0.45 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\wsgi.py (0.16 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\__init__.py (0 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GETTING_STARTED.md (6.32 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_AUTH.md (5.14 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_NOTIFICATION.md (8.46 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_SUBSCRIPTION.md (6.73 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_USERS.md (5.83 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\next\prompt_fisrt_task.md (0.5 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\next\prompt_initialisation.md (2.22 KB)
- C:\Users\hp\Documents\gabriel\AGT-SERVICES\next\prompt_todo.md (2.67 KB)

## CODE CONTEXT

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\Docker compose.infra.yml =====
`
# ============================================================
# AG TECHNOLOGIES â€” Infrastructure partagÃ©e
# Usage : docker compose -f docker-compose.infra.yml up -d
# Monte les services d'infrastructure communs Ã  tout l'Ã©cosystÃ¨me.
# Chaque microservice a son propre docker-compose.yml pour sa DB et son Redis.
# ============================================================

services:

  # â”€â”€ API Gateway (Nginx reverse proxy) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  gateway:
    image: nginx:alpine
    container_name: agt_gateway
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - rabbitmq
    networks:
      - agt_network

  # â”€â”€ RabbitMQ (Message Broker partagÃ©) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    container_name: agt_rabbitmq
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: agt_rabbit
      RABBITMQ_DEFAULT_PASS: agt_rabbit_password
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 15s
      timeout: 10s
      retries: 5
    networks:
      - agt_network

  # â”€â”€ Elasticsearch (Search Service) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
    container_name: agt_elasticsearch
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 5
    networks:
      - agt_network

volumes:
  rabbitmq_data:
    driver: local
  es_data:
    driver: local

networks:
  agt_network:
    name: agt_network
    driver: bridge
`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\nginx.conf =====
`
# ============================================================
# AG TECHNOLOGIES â€” API Gateway (Nginx)
# Reverse proxy unifiÃ© pour tout l'Ã©cosystÃ¨me.
# Chaque service est accessible via /api/v1/<service>/...
# ============================================================

events {
    worker_connections 1024;
}

http {
    # â”€â”€ Logging â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    log_format json_log escape=json '{'
        '"time":"$time_iso8601",'
        '"remote_addr":"$remote_addr",'
        '"method":"$request_method",'
        '"uri":"$request_uri",'
        '"status":$status,'
        '"upstream":"$upstream_addr",'
        '"response_time":$request_time'
    '}';
    access_log /var/log/nginx/access.log json_log;

    # â”€â”€ Rate limiting global â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    limit_req_zone $binary_remote_addr zone=global:10m rate=100r/m;

    # â”€â”€ CORS headers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    map $http_origin $cors_origin {
        default "";
        "~^https?://localhost(:[0-9]+)?$" "$http_origin";
        "~^https?://.*\.agt\.com$" "$http_origin";
    }

    # â”€â”€ Upstreams â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    upstream auth {
        server host.docker.internal:7000;
    }

    upstream users {
        server host.docker.internal:7001;
    }

    upstream notification {
        server host.docker.internal:7002;
    }

    upstream media {
        server host.docker.internal:7003;
    }

    upstream subscription {
        server host.docker.internal:7004;
    }

    upstream payment {
        server host.docker.internal:7005;
    }

    upstream wallet {
        server host.docker.internal:7006;
    }

    upstream search {
        server host.docker.internal:7007;
    }

    upstream chat {
        server host.docker.internal:7008;
    }

    upstream geoloc {
        server host.docker.internal:7009;
    }

    upstream chatbot {
        server host.docker.internal:7010;
    }

    # â”€â”€ Server â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    server {
        listen 80;
        server_name localhost;

        # CORS
        add_header Access-Control-Allow-Origin $cors_origin always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-Platform-Id, X-Admin-API-Key, X-Requested-With" always;
        add_header Access-Control-Allow-Credentials "true" always;

        if ($request_method = OPTIONS) {
            return 204;
        }

        # Rate limiting
        limit_req zone=global burst=20 nodelay;

        # â”€â”€ Auth Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/auth/ {
            proxy_pass http://auth/api/v1/auth/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Users Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/users {
            proxy_pass http://users/api/v1/users;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/platforms/ {
            proxy_pass http://users/api/v1/platforms/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Notification Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/notifications/ {
            proxy_pass http://notification/api/v1/notifications/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/templates/ {
            proxy_pass http://notification/api/v1/templates/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/campaigns/ {
            proxy_pass http://notification/api/v1/campaigns/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Media Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/media/ {
            proxy_pass http://media/api/v1/media/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            client_max_body_size 100M;
        }

        # â”€â”€ Subscription Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/subscriptions/ {
            proxy_pass http://subscription/api/v1/subscriptions/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/plans/ {
            proxy_pass http://subscription/api/v1/plans/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/quotas/ {
            proxy_pass http://subscription/api/v1/quotas/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Payment Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/payments/ {
            proxy_pass http://payment/api/v1/payments/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Wallet Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/wallets/ {
            proxy_pass http://wallet/api/v1/wallets/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Search Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/search/ {
            proxy_pass http://search/api/v1/search/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/indexes/ {
            proxy_pass http://search/api/v1/indexes/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Chat Service (REST) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/chat/ {
            proxy_pass http://chat/api/v1/chat/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Chat Service (WebSocket) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /socket.io/ {
            proxy_pass http://chat/socket.io/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # â”€â”€ Geoloc Service (REST) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/geoloc/ {
            proxy_pass http://geoloc/api/v1/geoloc/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Geoloc Service (WebSocket) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /geoloc/socket.io/ {
            proxy_pass http://geoloc/socket.io/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # â”€â”€ Chatbot Service â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /api/v1/chatbot/ {
            proxy_pass http://chatbot/api/v1/chatbot/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/v1/bots/ {
            proxy_pass http://chatbot/api/v1/bots/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # â”€â”€ Health global â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        location /health {
            return 200 '{"status":"gateway_ok"}';
            add_header Content-Type application/json;
        }
    }
}
`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\notes.md =====
`
# Notes gÃ©nÃ©rales et intÃ©rogations sur notre architecchture mico-services

## Service auth
AprÃ¨s avoir suivi avec succÃ¨s les instructions d'installation et de lancement de ce premier micro-service, je me suis posÃ© les questiosn suivantes :
- En effet, cahque micro service a sa propre basez de donÃ©e, cependant, va t'on cÃ©rer un conteneur docker de base de donnÃ©e pour chacun ? si oui est-ce optimal en terme de ressources ?
- comment configurer et comment Ã  utiliser ce premeir service d'authentification ?
- doit-on mettre sur pied un guide de configuration et d'utilisation du service d'authentification pour nos developpeurs internes ?

celÃ  m'a poussÃ© Ã  me poser les questions suivantes pour les services Ã  venir :

- comment configurer chaque microservice ?
- comment dÃ©ployer nos micro-services ensembles ?
- comprendre comment fonctionne chacun de nos micro-services ?
- comment utiliser notre Ã©co-systÃ¨me microservice ?
- faut-il mettre sur pied un backend mÃ©tier template qui intÃ¨gre tous nos micro-services ?
- faut-il mettre sur pied un frontend mÃ©tier template qui intÃ¨gre notre backend mÃ©tier ?
- faut-il mettre en place le monitoring de notre architechture micro-services ?
- ne doit-on pas faire un petite plateforme rapide de faq pour rÃ©pondre Ã  toutes ces questions pour nos dÃ©vÃ©loppeurs? danslaquelle on rÃ©pond Ã  chaque question en markdown et on versionne les rÃ©ponse, une sorte de forum internet Ã  Ag-technologies afin que chaque nouveau dÃ©velopperu puisse s'Ã©panouir ?
- est-il nÃ©cessaire de faire un service MESH pour Ag-technologies ? j'ai vu Ã§a sur youtube 

## Service users

En plus de me poser les mÃªmes questions que pour le service auth, aprÃ¨s avoir dÃ©marrÃ© le service users, j'ai remarquÃ© plusieurs manquements sur le swagger :

les groupes de routes
- Health
Etat du service
- Profile
CRUD profil utilisateur
- Sync
Synchronisation depuis Auth
- Addresses
CRUD adresses

ne sont pas testables ur le swagger car ces derniers n'exposent aucune route, juste le dropwon vide avec la description de cahque groupe comme mentionnÃ© Ã§i haut

# Services notifications
AprÃ¨s avoir lancÃ© ce service, je me suis posÃ© les mÃªmes questions que pour le service auth, mais j'ai trouvÃ© que ici le swagger semble complet. Par ailleurs; j'ai aussi vu le lien vers rabitmq, mais on me demande un mot de passe et un username pour y accÃ©der, Ã§a relance la question de guiude d'utilisation  persiste donc Ã  ce niveau                     
`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\README.md =====
`
# AG Technologies — Microservices Platform

Architecture microservices partagée pour l'écosystème AGT (AGT-Bot, AGT-Market, SALMA, futures plateformes).

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PLATEFORMES                          │
│         AGT-Bot · AGT-Market · SALMA · ...              │
└──────────┬──────────┬──────────┬──────────┬─────────────┘
           │          │          │          │
     ┌─────▼──┐ ┌─────▼──┐ ┌────▼───┐ ┌───▼────┐
     │  Auth  │ │ Users  │ │ Notifs │ │ Média  │
     │ Django │ │ Django │ │ Django │ │ NestJS │
     └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
         │          │          │           │
   ┌─────▼──┐ ┌─────▼──┐ ┌────▼───┐ ┌────▼───┐
   │  Sub.  │ │Payment │ │ Wallet │ │ Search │
   │ Django │ │ Django │ │ Django │ │Django+ES│
   └────────┘ └────────┘ └────────┘ └────────┘
         │          │          │
   ┌─────▼──┐ ┌─────▼──┐ ┌────▼───┐
   │  Chat  │ │ Geoloc │ │Chatbot │
   │Express │ │ NestJS │ │ Django │
   └────────┘ └────────┘ └────────┘
```

**Communication** : REST (synchrone) + RabbitMQ (asynchrone pour paiement, wallet, notifications, indexation).

---

## Services

| Service | Stack | Port | Rôle |
|---------|-------|------|------|
| **Auth** | Django/DRF | 7000 | Identité, JWT, sessions, OAuth, 2FA, S2S |
| **Users** | Django/DRF | 7001 | Profils, RBAC dynamique, documents, métadonnées |
| **Notification** | Django/DRF + Celery | 7002 | Envoi multi-canal (email, SMS, push, in-app, WhatsApp) |
| **Média** | NestJS | 7003 | Upload, traitement, stockage, thumbnails, CDN |
| **Subscription** | Django/DRF + Celery | 7004 | Plans, quotas, cycles, facturation |
| **Payment** | Django/DRF | 7005 | Providers (Orange Money, MTN MoMo, Stripe, PayPal) |
| **Wallet** | Django/DRF | 7006 | Ledger double-entry, virements, cash-in/out |
| **Search** | Django/DRF + Elasticsearch | 7007 | Indexation, recherche full-text, suggestions |
| **Chat** | Express/Socket.io | 7008 | Messagerie temps réel, présence, fichiers |
| **Geoloc** | NestJS/Socket.io + PostGIS | 7009 | Tracking GPS, geofencing, zones |
| **Chatbot** | Django/DRF + Celery | 7010 | Orchestrateur IA, flows, knowledge base, RAG |

---

## État actuel

**4 services codés** (héritage v0, en cours de correction) :

| Service | État | Travail restant |
|---------|------|-----------------|
| Auth | ✅ ~85% conforme | Corrections mineures (rate limiting, CSRF, bug cleanup) |
| Users | ⚠️ ~60% conforme | Refonte partielle — code basé sur Users v1.0 au lieu de v2.1 |
| Notification | ✅ ~80% conforme | Ajustements (convention user_id, vérification user actif) |
| Média | ✅ ~75% conforme | Ajustements (préfixe API, convention identité) |

**7 services à implémenter** : Subscription, Payment, Wallet, Search, Chat, Geoloc, Chatbot.

**Problème principal identifié** : le code existant a été développé avec Users v1.0. L'architecture validée exige Users v2.1 (suppression dual, hard delete sécurisé, plus de table platforms locale). La mise en conformité de Users est le chantier prioritaire car tous les services en dépendent.

---

## Convention de versionnement

Tous les services seront livrés en **v1.0**. Les numéros de version des CDC d'architecture (Auth v2.1, Users v2.1, Notifs v1.2, etc.) sont des versions de conception interne. La version de livraison du code est uniformément **1.0.0**.

---

## Documentation

| Document | Description |
|----------|-------------|
| **[TODO.md](./TODO.md)** | Plan de mise en place complet — 6 phases, 11 services, checkboxes |
| **[STANDARDS.md](./STANDARDS.md)** | Conventions techniques unifiées — identité, réponses API, events, ports |
| **[docker-compose.infra.yml](./docker-compose.infra.yml)** | Infrastructure partagée — Gateway Nginx, RabbitMQ, Elasticsearch |
| **[gateway/nginx.conf](./gateway/nginx.conf)** | Configuration du reverse proxy — routage vers tous les services |

---

## Démarrage rapide

```bash
# 1. Monter l'infrastructure partagée
docker compose -f docker-compose.infra.yml up -d

# 2. Monter un service (exemple : Auth)
cd agt-auth
cp .env.example .env
docker compose up -d

# 3. Vérifier
curl http://localhost/api/v1/auth/health
```

---

## Structure type d'un service

Chaque service respecte le template unifié :

```
service-name/
├── app/                    # Code applicatif (Django apps ou src/ NestJS)
├── domain/                 # Logique métier
├── infrastructure/         # DB, cache, clients externes
├── api/                    # Exposition REST
├── tests/
│   ├── unit/
│   └── integration/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── requirements.txt        # ou package.json
├── README.md
└── CDC_v1.0.md
```

---

## Principes

- **CDC > Code** — les cahiers des charges validés sont la référence absolue
- **1 service = 1 DB** — pas d'accès direct à la base d'un autre service
- **Auth est la source de vérité** pour l'identité et les plateformes
- **Users est la source de vérité** pour les profils, rôles et permissions
- **Idempotence obligatoire** sur paiement, wallet, notifications
- **Pas de logique métier dupliquée** entre services

---

*AG Technologies — Confidentiel — Usage interne*
`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\standards.md =====
`
# AG TECHNOLOGIES â€” STANDARDS & CONVENTIONS v1.0

> Ce document est la rÃ©fÃ©rence pour tout dÃ©veloppeur de l'Ã©cosystÃ¨me AGT.
> Chaque service DOIT respecter ces conventions. Aucune exception sans validation architecte.

---

## 1. Convention d'identitÃ© (CRITIQUE)

### RÃ¨gle unique

| Identifiant | Signifie | Origine |
|-------------|----------|---------|
| `user_id` | `users_auth.id` | Champ `sub` du JWT |
| `platform_id` | `platforms.id` | Registre Auth, champ `platform_id` du JWT |
| `auth_user_id` | `users_auth.id` | Alias utilisÃ© dans Users pour la FK logique |
| `users_profiles.id` | ID interne Users | Jamais exposÃ© aux autres services |

**RÃ¨gle** : tout service qui stocke ou reÃ§oit un `user_id` utilise `users_auth.id` (= `sub` JWT).
Le Service Users est le seul Ã  manipuler `users_profiles.id` en interne. Les autres services n'ont jamais besoin de connaÃ®tre cet ID.

**RÃ©solution** : si un service a besoin du profil Users, il appelle `GET /api/v1/users/by-auth/{authUserId}`.

---

## 2. Structure de projet

### Services Django/DRF

```
service-name/
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ <module_1>/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ models.py          # ModÃ¨les Django ORM
â”‚   â”‚   â”œâ”€â”€ serializers.py     # Serializers DRF
â”‚   â”‚   â”œâ”€â”€ views.py           # Views (ou views_*.py si volumineux)
â”‚   â”‚   â”œâ”€â”€ urls.py            # Routes du module
â”‚   â”‚   â”œâ”€â”€ services.py        # Logique mÃ©tier, clients inter-services
â”‚   â”‚   â”œâ”€â”€ permissions.py     # Permissions custom
â”‚   â”‚   â”œâ”€â”€ pagination.py      # Pagination standard
â”‚   â”‚   â””â”€â”€ tests/
â”‚   â”‚       â”œâ”€â”€ test_models.py
â”‚   â”‚       â”œâ”€â”€ test_views.py
â”‚   â”‚       â””â”€â”€ test_services.py
â”‚   â””â”€â”€ <module_2>/
â”‚       â””â”€â”€ ...
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ settings.py            # Settings Django
â”‚   â”œâ”€â”€ urls.py                # Root URL conf
â”‚   â”œâ”€â”€ wsgi.py
â”‚   â””â”€â”€ celery.py              # Si Celery requis
â”œâ”€â”€ workers/                   # Si Celery requis
â”‚   â”œâ”€â”€ __init__.py
â”‚   â””â”€â”€ tasks.py
â”œâ”€â”€ common/                    # Code partagÃ© intra-service
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ middleware.py          # Rate limiting, logging, CORS
â”‚   â”œâ”€â”€ exceptions.py         # Handlers d'erreurs
â”‚   â””â”€â”€ utils.py
â”œâ”€â”€ keys/                      # ClÃ©s RSA (gitignored)
â”œâ”€â”€ docker/
â”‚   â””â”€â”€ Dockerfile
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â”œâ”€â”€ manage.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ pytest.ini
â”œâ”€â”€ README.md
â””â”€â”€ CDC_v1.0.md
```

### Services Node.js/NestJS

```
service-name/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ <module_1>/
â”‚   â”‚   â”œâ”€â”€ <module>.module.ts
â”‚   â”‚   â”œâ”€â”€ <module>.controller.ts
â”‚   â”‚   â”œâ”€â”€ <module>.service.ts
â”‚   â”‚   â”œâ”€â”€ entities/
â”‚   â”‚   â”‚   â””â”€â”€ <entity>.entity.ts
â”‚   â”‚   â””â”€â”€ dto/
â”‚   â”‚       â””â”€â”€ <dto>.dto.ts
â”‚   â”œâ”€â”€ common/
â”‚   â”‚   â”œâ”€â”€ guards/
â”‚   â”‚   â”œâ”€â”€ middleware/
â”‚   â”‚   â”œâ”€â”€ filters/
â”‚   â”‚   â””â”€â”€ utils/
â”‚   â”œâ”€â”€ app.module.ts
â”‚   â””â”€â”€ main.ts
â”œâ”€â”€ test/
â”‚   â”œâ”€â”€ unit/
â”‚   â””â”€â”€ integration/
â”œâ”€â”€ keys/
â”œâ”€â”€ docker/
â”‚   â””â”€â”€ Dockerfile
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â”œâ”€â”€ package.json
â”œâ”€â”€ tsconfig.json
â”œâ”€â”€ nest-cli.json
â”œâ”€â”€ README.md
â””â”€â”€ CDC_v1.0.md
```

### Services Node.js/Express (Chat)

```
service-name/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ modules/
â”‚   â”‚   â”œâ”€â”€ <module>/
â”‚   â”‚   â”‚   â”œâ”€â”€ <module>.routes.js
â”‚   â”‚   â”‚   â”œâ”€â”€ <module>.controller.js
â”‚   â”‚   â”‚   â”œâ”€â”€ <module>.service.js
â”‚   â”‚   â”‚   â””â”€â”€ <module>.model.js
â”‚   â”‚   â””â”€â”€ ...
â”‚   â”œâ”€â”€ common/
â”‚   â”‚   â”œâ”€â”€ middleware/
â”‚   â”‚   â”œâ”€â”€ guards/
â”‚   â”‚   â””â”€â”€ utils/
â”‚   â”œâ”€â”€ socket/                # Socket.io handlers
â”‚   â”‚   â”œâ”€â”€ index.js
â”‚   â”‚   â”œâ”€â”€ presence.js
â”‚   â”‚   â””â”€â”€ messaging.js
â”‚   â”œâ”€â”€ app.js
â”‚   â””â”€â”€ server.js
â”œâ”€â”€ test/
â”‚   â”œâ”€â”€ unit/
â”‚   â””â”€â”€ integration/
â”œâ”€â”€ keys/
â”œâ”€â”€ docker/
â”‚   â””â”€â”€ Dockerfile
â”œâ”€â”€ docker-compose.yml
â”œâ”€â”€ .env.example
â”œâ”€â”€ .gitignore
â”œâ”€â”€ package.json
â”œâ”€â”€ README.md
â””â”€â”€ CDC_v1.0.md
```

---

## 3. Format des rÃ©ponses API

### SuccÃ¨s simple

```json
{
  "message": "Operation successful"
}
```

### SuccÃ¨s avec donnÃ©e

```json
{
  "id": "uuid",
  "field": "value",
  "created_at": "2026-04-06T10:00:00Z"
}
```

### SuccÃ¨s avec liste paginÃ©e

```json
{
  "data": [...],
  "page": 1,
  "limit": 20,
  "total": 142
}
```

### Erreur

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description lisible"
  }
}
```

### Codes d'erreur standard

| Code HTTP | Code erreur | Usage |
|-----------|-------------|-------|
| 400 | `VALIDATION_ERROR` | DonnÃ©es invalides |
| 401 | `UNAUTHORIZED` | Token manquant ou invalide |
| 403 | `FORBIDDEN` | Droits insuffisants |
| 404 | `NOT_FOUND` | Ressource introuvable |
| 409 | `CONFLICT` | Doublon, idempotence violÃ©e |
| 429 | `RATE_LIMITED` | Trop de requÃªtes |
| 500 | `INTERNAL_ERROR` | Erreur serveur |

---

## 4. Health Check

Chaque service expose `GET /api/v1/health` (ou `GET /api/v1/<service>/health` pour Auth).

Format obligatoire :

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

Si un composant est en erreur : `"status": "degraded"` + HTTP 503.

Champs optionnels selon le service : `"broker"`, `"elasticsearch"`, `"storage"`.

---

## 5. Authentification inter-services

### JWT utilisateur

- SignÃ© RS256 par Auth
- Tous les services valident avec la clÃ© publique Auth
- Payload standard :

```json
{
  "sub": "users_auth.id",
  "iss": "agt-auth",
  "aud": "agt-ecosystem",
  "iat": 1710840000,
  "exp": 1710840900,
  "jti": "unique-token-id",
  "session_id": "session-uuid",
  "platform_id": "platform-uuid",
  "email": "user@example.com",
  "email_verified": true,
  "two_fa_verified": false
}
```

### Token S2S (service-to-service)

- Obtenu via `POST /api/v1/auth/s2s/token`
- ValidÃ© via `POST /api/v1/auth/s2s/introspect`
- UtilisÃ© pour les appels inter-services sans contexte utilisateur

### Admin API Key

- Header `X-Admin-API-Key`
- Pour les opÃ©rations d'administration (block, purge, plateformes)
- Variable d'environnement `ADMIN_API_KEY`

---

## 6. Ã‰vÃ©nements RabbitMQ

### Format standard d'Ã©vÃ©nement

```json
{
  "event_id": "uuid-v4",
  "event_type": "payment.confirmed",
  "timestamp": "2026-04-06T10:00:00Z",
  "source": "payment-service",
  "data": { ... },
  "idempotency_key": "uuid-unique"
}
```

### RÃ¨gles

- Chaque Ã©vÃ©nement DOIT contenir `event_id`, `timestamp`, `source`
- Les consommateurs DOIVENT Ãªtre idempotents (dÃ©duplication sur `event_id`)
- Retry automatique avec backoff exponentiel (1s, 2s, 4s)
- Dead letter queue pour les messages en Ã©chec aprÃ¨s 3 retries

### Ã‰vÃ©nements dÃ©finis

| Source | Ã‰vÃ©nement | Consommateurs |
|--------|-----------|---------------|
| Subscription | `subscription.billing_requested` | Payment |
| Payment | `payment.confirmed` | Wallet, Notification |
| Payment | `payment.failed` | Subscription, Notification |
| Payment | `payment.cancelled` | Subscription, Notification |
| Wallet | `wallet.credited` | Notification |
| Wallet | `wallet.debited` | Notification |
| Geoloc | `geofence.entered` | Plateformes, Notification |
| Geoloc | `geofence.exited` | Plateformes, Notification |
| Plateformes | `index.upsert` | Search |
| Plateformes | `index.delete` | Search |

---

## 7. Ports par service

| Service | Port app | Port DB (host) | Port Redis (host) |
|---------|----------|----------------|-------------------|
| Auth | 7000 | 5432 | 6379 |
| Users | 7001 | 5433 | 6380 |
| Notification | 7002 | 5434 | 6381 |
| MÃ©dia | 7003 | 5435 | 6382 |
| Subscription | 7004 | 5436 | 6383 |
| Payment | 7005 | 5437 | 6384 |
| Wallet | 7006 | 5438 | 6385 |
| Search | 7007 | 5439 | 6386 |
| Chat | 7008 | 5440 | 6387 |
| Geoloc | 7009 | 5441 | 6388 |
| Chatbot | 7010 | 5442 | 6389 |
| **Infra partagÃ©e** | | | |
| RabbitMQ | 5672 / 15672 | â€” | â€” |
| Elasticsearch | 9200 | â€” | â€” |
| API Gateway | 80 / 443 | â€” | â€” |

---

## 8. Variables d'environnement communes

Chaque `.env.example` DOIT contenir au minimum :

```env
# === Service ===
SERVICE_NAME=agt-auth
SERVICE_PORT=7000
DEBUG=False
SECRET_KEY=change-me-in-production

# === Database ===
DATABASE_URL=postgresql://user:password@db:5432/dbname

# === Redis ===
REDIS_URL=redis://redis:6379/0

# === Auth (tous sauf Auth lui-mÃªme) ===
AUTH_SERVICE_URL=http://localhost:7000
AUTH_PUBLIC_KEY_PATH=./keys/auth_public.pem

# === Inter-services (selon besoins) ===
USERS_SERVICE_URL=http://localhost:7001
NOTIFICATION_SERVICE_URL=http://localhost:7002
MEDIA_SERVICE_URL=http://localhost:7003

# === RabbitMQ (si event-driven) ===
BROKER_URL=amqp://guest:guest@rabbitmq:5672//
```

---

## 9. Docker

### Dockerfile Django (template)

```dockerfile
# â”€â”€ Builder â”€â”€
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# â”€â”€ Production â”€â”€
FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE ${SERVICE_PORT:-7000}
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7000", "--workers", "4"]
```

### Dockerfile NestJS (template)

```dockerfile
# â”€â”€ Builder â”€â”€
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# â”€â”€ Production â”€â”€
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json .
EXPOSE ${SERVICE_PORT:-7003}
CMD ["node", "dist/main"]
```

---

## 10. Tests

### Structure obligatoire

```
tests/
â”œâ”€â”€ unit/          # Logique mÃ©tier, modÃ¨les, services
â””â”€â”€ integration/   # Endpoints, DB, inter-services
```

### ExÃ©cution

```bash
# Django
pytest

# NestJS
npm test

# Express
npm test
```

### RÃ¨gle de validation

> Un service sans tests n'est pas considÃ©rÃ© comme terminÃ©.

---

## 11. README template

Chaque service DOIT avoir un README contenant :

1. **Nom et description** (1-2 lignes)
2. **PrÃ©requis** (Docker, clÃ©s RSA...)
3. **Installation et dÃ©marrage** (3-5 commandes max)
4. **Variables d'environnement** (tableau)
5. **Endpoints principaux** (tableau)
6. **Lancer les tests** (1 commande)
7. **DÃ©pendances inter-services** (qui j'appelle, qui m'appelle)

---

## 12. Git & Versionnement

- Branche principale : `main`
- Convention de commit : `[service] action: description`
  - Ex : `[auth] fix: corriger bug cleanup_expired`
  - Ex : `[users] feat: ajouter endpoint by-auth`
- Un service = un dossier Ã  la racine du monorepo
- Tags de release : `auth-v1.0.0`, `users-v1.0.0`, etc.

---

*AG Technologies â€” Standards v1.0 â€” Avril 2026*
`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\todo.md =====
`
# AG TECHNOLOGIES â€” PLAN DE MISE EN PLACE v1.0

> **RÃ¨gle** : Tous les services seront livrÃ©s en **version 1.0**.
> Chaque service = CDC v1.0 mis Ã  jour + Code ZIP complet conforme + Template de structure unifiÃ©.

---

## PHASE 0 â€” FONDATIONS & STANDARDS

### 0.1 Template de structure de projet unifiÃ©

- [ ] DÃ©finir le template Django/DRF (Auth, Users, Notification, Search, Chatbot, Subscription, Payment, Wallet)
- [ ] DÃ©finir le template Node.js/NestJS (MÃ©dia, Geoloc)
- [ ] DÃ©finir le template Node.js/Express (Chat)
- [ ] Valider la structure commune :
  ```
  service-name/
  â”œâ”€â”€ app/              # ou src/ (NestJS)
  â”œâ”€â”€ domain/
  â”œâ”€â”€ infrastructure/
  â”œâ”€â”€ api/
  â”œâ”€â”€ tests/
  â”‚   â”œâ”€â”€ unit/
  â”‚   â””â”€â”€ integration/
  â”œâ”€â”€ docker/
  â”‚   â”œâ”€â”€ Dockerfile
  â”‚   â””â”€â”€ docker-compose.yml
  â”œâ”€â”€ .env.example
  â”œâ”€â”€ requirements.txt  # ou package.json
  â”œâ”€â”€ README.md
  â””â”€â”€ CDC_v1.0.md       # CDC embarquÃ© dans le service
  ```
- [ ] DÃ©finir les conventions de nommage (endpoints, variables, fichiers)
- [ ] DÃ©finir le format standard des rÃ©ponses d'erreur
- [ ] DÃ©finir le format standard de pagination
- [ ] DÃ©finir le health check standard (DB + Redis + version)
- [ ] DÃ©finir la convention d'identitÃ© unifiÃ©e (`user_id = users_auth.id` = `sub` JWT sauf Users qui utilise `users_profiles.id` en interne)
- [ ] DÃ©finir le `.env.example` type par stack
- [ ] DÃ©finir le `docker-compose.yml` type par stack
- [ ] DÃ©finir le README template (run local, endpoints, tests, env vars)

### 0.2 RenumÃ©rotation des CDC

- [ ] CrÃ©er le mapping de versions :
  - Auth v2.1 â†’ **Auth v1.0**
  - Users v2.1 â†’ **Users v1.0**
  - Notification v1.2 â†’ **Notifs v1.0**
  - MÃ©dia v1.4 â†’ **MÃ©dia v1.0**
  - Search v1.2 â†’ **Search v1.0**
  - Chat v1.2 â†’ **Chat v1.0**
  - Chatbot v1.2 â†’ **Chatbot v1.0**
  - Subscription v1.2 â†’ **Subscription v1.0**
  - Payment v1.2 â†’ **Payment v1.0**
  - Wallet v1.1 â†’ **Wallet v1.0**
  - Geoloc v1.2 â†’ **Geoloc v1.0**

---

## PHASE 1 â€” SERVICES FONDATION

### 1.1 Service Auth v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0, historique condensÃ©
- [ ] IntÃ©grer la convention d'identitÃ© unifiÃ©e dans le CDC
- [ ] IntÃ©grer le template de structure dans le CDC
- [ ] Valider les contrats inter-services (Auth â†’ Users, Auth â†’ Notification)

#### Code â€” Audit & Corrections
- [ ] Corriger le bug `cleanup_expired.py` (import `models` mal placÃ©)
- [ ] ImplÃ©menter le rate limiting Redis (sliding window) sur les endpoints critiques
- [ ] ImplÃ©menter la protection CSRF (header `X-Requested-With` sur endpoints cookie-based)
- [ ] VÃ©rifier le contrat `UsersServiceClient` â€” push `POST /api/v1/users/status-sync`
- [ ] VÃ©rifier le contrat `UsersServiceClient` â€” provisioning `POST /api/v1/users`
- [ ] VÃ©rifier le contrat `UsersServiceClient` â€” sync email/phone `POST /api/v1/users/sync`
- [ ] Aligner la structure du projet sur le template unifiÃ©
- [ ] Mettre Ã  jour le health check â†’ version `"1.0.0"`
- [ ] VÃ©rifier et complÃ©ter les tests unitaires
- [ ] VÃ©rifier et complÃ©ter les tests d'intÃ©gration
- [ ] VÃ©rifier le `.env.example` (toutes les variables documentÃ©es)
- [ ] VÃ©rifier le `docker-compose.yml`
- [ ] Mettre Ã  jour le `README.md` selon le template
- [ ] VÃ©rifier les migrations Django

#### Livraison
- [ ] Produire le CDC Auth v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 1.2 Service Users v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0, intÃ©grer les changements v2.1
- [ ] Documenter la convention `{id} = users_profiles.id`
- [ ] Documenter le modÃ¨le de suppression dual (quitter plateforme vs soft delete global)
- [ ] Documenter la sÃ©quence hard delete sÃ©curisÃ©e
- [ ] Documenter les champs `hard_delete_after`, `purge_auth_pending`, `deletion_error_reason`

#### Code â€” Corrections structurelles (v1.0 â†’ v2.1)
- [ ] Supprimer la table `platforms` locale â€” utiliser les UUID Auth directement
- [ ] Ajouter les champs manquants Ã  `UserProfile` :
  - [ ] `hard_delete_after` (TIMESTAMPTZ)
  - [ ] `purge_auth_pending` (BOOLEAN, default false)
  - [ ] `deletion_error_reason` (TEXT)
  - [ ] `deletion_in_progress` dans `UserStatusChoice`
- [ ] Ajouter la table `audit_logs`
- [ ] Ajouter la table `document_history`
- [ ] Ajouter l'endpoint `GET /api/v1/users/by-auth/{authUserId}`
- [ ] Ajouter l'endpoint `DELETE /api/v1/users/{id}/platforms/{platformId}` (quitter une plateforme)
- [ ] Corriger `UserRole.unique_together` : `(user, role)` au lieu de `(user, role, platform)`
- [ ] Bloquer `email` et `phone` en Ã©criture dans `UserProfileUpdateSerializer`
- [ ] ImplÃ©menter la sÃ©quence hard delete sÃ©curisÃ©e (Users â†’ deletion_in_progress â†’ purge Auth â†’ purge Users)
- [ ] Aligner la structure sur le template unifiÃ©
- [ ] Mettre Ã  jour le health check â†’ version `"1.0.0"`
- [ ] VÃ©rifier et complÃ©ter les tests unitaires
- [ ] VÃ©rifier et complÃ©ter les tests d'intÃ©gration
- [ ] VÃ©rifier le `.env.example`
- [ ] VÃ©rifier le `docker-compose.yml`
- [ ] Mettre Ã  jour le `README.md`
- [ ] GÃ©nÃ©rer les migrations Django

#### Livraison
- [ ] Produire le CDC Users v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 2 â€” SERVICES DE SUPPORT

### 2.1 Service Notification v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0
- [ ] Clarifier la convention `user_id = users_profiles.id`
- [ ] Aligner les contrats inter-services

#### Code â€” Corrections
- [ ] VÃ©rifier la rÃ©solution `user_id` (users_profiles.id vs users_auth.id)
- [ ] VÃ©rifier l'implÃ©mentation de la table `device_tokens`
- [ ] VÃ©rifier l'implÃ©mentation de `PlatformChannelConfig`
- [ ] VÃ©rifier la logique de fallback inter-canal dans le worker
- [ ] VÃ©rifier la vÃ©rification user actif avant envoi (v1.2)
- [ ] Aligner la structure sur le template unifiÃ©
- [ ] Mettre Ã  jour le health check â†’ version `"1.0.0"`
- [ ] VÃ©rifier les tests
- [ ] VÃ©rifier `.env.example` et `docker-compose.yml`
- [ ] Mettre Ã  jour le `README.md`

#### Livraison
- [ ] Produire le CDC Notification v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 2.2 Service MÃ©dia v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0
- [ ] Confirmer la convention `uploaded_by = users_auth.id`, `owner_user_id = users_auth.id`

#### Code â€” Corrections
- [ ] Ajouter le prÃ©fixe `/api/v1` sur tous les endpoints
- [ ] VÃ©rifier `owner_user_id` dans le modÃ¨le `MediaFile`
- [ ] VÃ©rifier le contrat Users â†” MÃ©dia (avatar_media_id, RGPD)
- [ ] VÃ©rifier le hard delete S2S-only
- [ ] Aligner la structure sur le template unifiÃ© (NestJS)
- [ ] Mettre Ã  jour le health check â†’ version `"1.0.0"`
- [ ] VÃ©rifier les tests
- [ ] VÃ©rifier `.env.example` et `docker-compose.yml`
- [ ] Mettre Ã  jour le `README.md`

#### Livraison
- [ ] Produire le CDC MÃ©dia v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 3 â€” SERVICES MÃ‰TIER CÅ’UR

### 3.1 Service Subscription v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0
- [ ] Aligner avec Auth v1.0 et Users v1.0

#### Code â€” ImplÃ©mentation from scratch
- [ ] ImplÃ©menter les modÃ¨les (Plan, PlanVersion, Subscriber, SubscriptionCycle, QuotaDefinition, QuotaUsage, QuotaReservation)
- [ ] ImplÃ©menter les endpoints REST
- [ ] ImplÃ©menter la vÃ©rification de quotas (reserve/confirm/release)
- [ ] ImplÃ©menter les Ã©vÃ©nements RabbitMQ (â†’ Payment, â†’ Notification)
- [ ] ImplÃ©menter les workers Celery (renewal, expiration, trial)
- [ ] ImplÃ©menter la stratÃ©gie de rÃ©silience (4 niveaux)
- [ ] ImplÃ©menter le rate limiting
- [ ] Ã‰crire les tests unitaires et d'intÃ©gration
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`
- [ ] Respecter le template de structure

#### Livraison
- [ ] Produire le CDC Subscription v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 3.2 Service Payment v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0
- [ ] Aligner avec Auth v1.0, Subscription v1.0

#### Code â€” ImplÃ©mentation from scratch
- [ ] ImplÃ©menter les modÃ¨les (PaymentIntent, Transaction, WebhookEvent, ProviderConfig, PaymentMethod)
- [ ] ImplÃ©menter les endpoints REST (initiate, status, cancel, webhooks)
- [ ] ImplÃ©menter les providers (Orange Money, MTN MoMo, Stripe, PayPal)
- [ ] ImplÃ©menter les webhooks normalisÃ©s
- [ ] ImplÃ©menter l'idempotence (`idempotency_key`)
- [ ] ImplÃ©menter les Ã©vÃ©nements RabbitMQ sortants (payment.confirmed/failed/cancelled)
- [ ] ImplÃ©menter la rÃ©conciliation
- [ ] Ã‰crire les tests unitaires et d'intÃ©gration
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Payment v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 3.3 Service Wallet v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0
- [ ] Aligner avec Auth v1.0, Payment v1.0

#### Code â€” ImplÃ©mentation from scratch
- [ ] ImplÃ©menter les modÃ¨les (Account, LedgerTransaction, Hold, CashoutRequest, AutoSplit)
- [ ] ImplÃ©menter le ledger double-entry (OBLIGATOIRE â€” aucune modification/suppression d'Ã©criture)
- [ ] ImplÃ©menter les endpoints REST (balance, transactions, transfer, cash-in, cash-out, holds)
- [ ] ImplÃ©menter la consommation des Ã©vÃ©nements RabbitMQ (payment.confirmed â†’ crÃ©dit wallet)
- [ ] ImplÃ©menter les Ã©missions d'Ã©vÃ©nements (wallet.credited, wallet.debited)
- [ ] ImplÃ©menter l'idempotence
- [ ] Ã‰crire les tests unitaires et d'intÃ©gration
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Wallet v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 4 â€” SERVICES APPLICATIFS

### 4.1 Service Search v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0

#### Code â€” ImplÃ©mentation from scratch
- [ ] ImplÃ©menter les modÃ¨les (SearchIndex, IndexConfig, PopularSearch)
- [ ] ImplÃ©menter les endpoints REST (search, index CRUD, suggestions, boost)
- [ ] ImplÃ©menter l'intÃ©gration Elasticsearch
- [ ] ImplÃ©menter la consommation des Ã©vÃ©nements RabbitMQ (indexation async via Celery)
- [ ] ImplÃ©menter la gouvernance des index (nommage, quotas)
- [ ] Ã‰crire les tests unitaires et d'intÃ©gration
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Search v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 4.2 Service Chat v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0

#### Code â€” ImplÃ©mentation from scratch (Node.js/Express/Socket.io)
- [ ] ImplÃ©menter les modÃ¨les (Conversation, Participant, Message, Attachment, Reaction, ReadReceipt)
- [ ] ImplÃ©menter les endpoints REST (conversations, messages, attachments)
- [ ] ImplÃ©menter les WebSockets (Socket.io) : prÃ©sence, typing, messages temps rÃ©el
- [ ] ImplÃ©menter le Redis Adapter (multi-instance)
- [ ] ImplÃ©menter l'intÃ©gration MÃ©dia (fichiers)
- [ ] ImplÃ©menter le transfert opÃ©rateur
- [ ] Ã‰crire les tests
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Chat v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 4.3 Service Geoloc v1.0

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0

#### Code â€” ImplÃ©mentation from scratch (Node.js/NestJS/Socket.io/PostGIS)
- [ ] ImplÃ©menter les modÃ¨les (TrackedEntity, GeoZone, GeoEvent, PositionHistory)
- [ ] ImplÃ©menter les endpoints REST (zones CRUD, position history, nearby)
- [ ] ImplÃ©menter les WebSockets (Socket.io) : position updates, geofence events
- [ ] ImplÃ©menter le geofencing (R-tree/quadtree in-memory)
- [ ] ImplÃ©menter les Ã©vÃ©nements RabbitMQ (geofence triggers)
- [ ] ImplÃ©menter PostGIS pour le stockage spatial
- [ ] Ã‰crire les tests
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Geoloc v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 5 â€” ORCHESTRATEUR IA (DERNIER)

### 5.1 Service Chatbot v1.0

> âš ï¸ Ne commence qu'aprÃ¨s stabilisation de : Auth, Users, Chat, Notification, MÃ©dia

#### CDC
- [ ] Mettre Ã  jour le CDC : version â†’ 1.0
- [ ] Aligner avec Chat v1.0, Search v1.0, MÃ©dia v1.0

#### Code â€” ImplÃ©mentation from scratch
- [ ] ImplÃ©menter les modÃ¨les (Bot, BotConfig, BotChannel, Flow, FlowNode, FlowAction, Intent, KnowledgeCategory, KnowledgeBaseEntry, AiProviderConfig, ConversationSession, ConversationLog, BotAction, BotStats, IngestionJob, TransferLog)
- [ ] ImplÃ©menter le Conversation Orchestrator
- [ ] ImplÃ©menter l'Action System standardisÃ©
- [ ] ImplÃ©menter les 3 couches de rÃ©ponse (rules â†’ KB â†’ IA)
- [ ] ImplÃ©menter les endpoints REST (bots CRUD, flows, intents, knowledge, stats)
- [ ] ImplÃ©menter le endpoint `POST /chatbot/converse`
- [ ] ImplÃ©menter le multi-provider IA (OpenAI, Anthropic) avec circuit breaker
- [ ] ImplÃ©menter le RAG (knowledge base + embeddings)
- [ ] ImplÃ©menter les workers Celery (ingestion docs, stats, health check providers)
- [ ] Ã‰crire les tests
- [ ] CrÃ©er `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Chatbot v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 6 â€” VALIDATION GLOBALE

### 6.1 Tests inter-services
- [ ] VÃ©rifier la compatibilitÃ© Auth â†” Users (provisioning, sync, purge)
- [ ] VÃ©rifier la compatibilitÃ© Auth â†” Notification
- [ ] VÃ©rifier la compatibilitÃ© Subscription â†” Payment (RabbitMQ)
- [ ] VÃ©rifier la compatibilitÃ© Payment â†” Wallet (RabbitMQ)
- [ ] VÃ©rifier la compatibilitÃ© Chat â†” Chatbot (transfert)
- [ ] VÃ©rifier tous les contrats S2S

### 6.2 Documentation finale
- [ ] VÃ©rifier que chaque ZIP contient son CDC v1.0
- [ ] VÃ©rifier que chaque service dÃ©marre sans erreur
- [ ] VÃ©rifier que chaque `.env.example` est complet
- [ ] VÃ©rifier que chaque `README.md` est exploitable
- [ ] Produire le document de synthÃ¨se inter-services (contrats, ports, dÃ©pendances)

---

## RÃ‰SUMÃ‰ DES LIVRABLES PAR SERVICE

| # | Service | Stack | CDC v1.0 | ZIP Code | Statut |
|---|---------|-------|----------|----------|--------|
| 1 | Auth | Django/DRF | â¬œ | â¬œ | Correction |
| 2 | Users | Django/DRF | â¬œ | â¬œ | Refonte partielle |
| 3 | Notification | Django/DRF + Celery | â¬œ | â¬œ | Correction |
| 4 | MÃ©dia | NestJS | â¬œ | â¬œ | Correction |
| 5 | Subscription | Django/DRF + Celery/RabbitMQ | â¬œ | â¬œ | From scratch |
| 6 | Payment | Django/DRF + RabbitMQ | â¬œ | â¬œ | From scratch |
| 7 | Wallet | Django/DRF + RabbitMQ | â¬œ | â¬œ | From scratch |
| 8 | Search | Django/DRF + Elasticsearch + Celery | â¬œ | â¬œ | From scratch |
| 9 | Chat | Express/Socket.io | â¬œ | â¬œ | From scratch |
| 10 | Geoloc | NestJS/Socket.io/PostGIS | â¬œ | â¬œ | From scratch |
| 11 | Chatbot | Django/DRF + Celery | â¬œ | â¬œ | From scratch |

---

*AG Technologies â€” Plan de mise en place v1.0 â€” Avril 2026*
`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\.env =====
`
# ============================================================
# AGT Auth Service v1.0 â€” Variables d'environnement
# ============================================================

# â”€â”€â”€ Django â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SECRET_KEY=change-me-in-production-use-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# â”€â”€â”€ Base de donnÃ©es â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
DATABASE_URL=postgresql://agt_user:agt_password@db:5432/agt_auth_db

# â”€â”€â”€ Redis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REDIS_URL=redis://redis:6379/0

# â”€â”€â”€ JWT (RS256) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
JWT_PRIVATE_KEY_PATH=/app/keys/private.pem
JWT_PUBLIC_KEY_PATH=/app/keys/public.pem
JWT_ACCESS_TTL=900
JWT_REFRESH_TTL=604800
JWT_ISSUER=agt-auth
JWT_AUDIENCE=agt-ecosystem

# â”€â”€â”€ Bcrypt â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BCRYPT_ROUNDS=12

# â”€â”€â”€ Admin â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ADMIN_API_KEY=change-me-admin-api-key-very-secret

# â”€â”€â”€ Services inter-microservices â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NOTIFICATION_SERVICE_URL=http://notification-service:7002/api/v1
USERS_SERVICE_URL=http://users-service:7001/api/v1

# â”€â”€â”€ OAuth Google â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:7000/api/v1/auth/oauth/google/callback

# â”€â”€â”€ OAuth Facebook â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_REDIRECT_URI=http://localhost:7000/api/v1/auth/oauth/facebook/callback

# â”€â”€â”€ OTP / Magic Link â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
OTP_TTL=300
MAGIC_LINK_TTL=600

# â”€â”€â”€ Rate Limiting â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
RATE_LIMIT_LOGIN=10
BRUTE_FORCE_MAX=5
BRUTE_FORCE_LOCKOUT=900

# â”€â”€â”€ Tokens â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
MAX_REFRESH_TOKENS=5

# â”€â”€â”€ Cookies â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
COOKIE_SECURE=False
COOKIE_SAMESITE=Lax

# â”€â”€â”€ CORS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\.env.example =====
`
# ============================================================
# AGT Auth Service v1.0 â€” Variables d'environnement
# ============================================================

# â”€â”€â”€ Django â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SECRET_KEY=change-me-in-production-use-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# â”€â”€â”€ Base de donnÃ©es â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
DATABASE_URL=postgresql://agt_user:agt_password@db:5432/agt_auth_db

# â”€â”€â”€ Redis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REDIS_URL=redis://redis:6379/0

# â”€â”€â”€ JWT (RS256) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
JWT_PRIVATE_KEY_PATH=/app/keys/private.pem
JWT_PUBLIC_KEY_PATH=/app/keys/public.pem
JWT_ACCESS_TTL=900
JWT_REFRESH_TTL=604800
JWT_ISSUER=agt-auth
JWT_AUDIENCE=agt-ecosystem

# â”€â”€â”€ Bcrypt â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BCRYPT_ROUNDS=12

# â”€â”€â”€ Admin â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ADMIN_API_KEY=change-me-admin-api-key-very-secret

# â”€â”€â”€ Services inter-microservices â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NOTIFICATION_SERVICE_URL=http://notification-service:7002/api/v1
USERS_SERVICE_URL=http://users-service:7001/api/v1

# â”€â”€â”€ OAuth Google â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:7000/api/v1/auth/oauth/google/callback

# â”€â”€â”€ OAuth Facebook â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_REDIRECT_URI=http://localhost:7000/api/v1/auth/oauth/facebook/callback

# â”€â”€â”€ OTP / Magic Link â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
OTP_TTL=300
MAGIC_LINK_TTL=600

# â”€â”€â”€ Rate Limiting â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
RATE_LIMIT_LOGIN=10
BRUTE_FORCE_MAX=5
BRUTE_FORCE_LOCKOUT=900

# â”€â”€â”€ Tokens â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
MAX_REFRESH_TOKENS=5

# â”€â”€â”€ Cookies â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
COOKIE_SECURE=False
COOKIE_SAMESITE=Lax

# â”€â”€â”€ CORS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\CDC_v1.0.md =====
`
# AGT Auth Service - Cahier des Charges v1.0

> Version de livraison : 1.0 | Statut : Implementation-ready | Classification : Confidentiel

## 1. Perimetre

Le service Auth couvre le cycle de vie de l'identite pure : inscription, connexion, gestion de sessions, securite (2FA, rate limiting), administration des plateformes clientes et tracabilite.

**Hors perimetre** : profils etendus (Users), roles/permissions (Users), envoi emails/SMS (Notification), logique metier des plateformes.

## 2. Stack

| Composant | Technologie |
|-----------|-------------|
| Framework | Python 3.11+ / Django 5.x / DRF |
| DB | PostgreSQL 15+ |
| Cache | Redis 7+ |
| JWT | RS256 (PyJWT) |
| Hashing | bcrypt (cost 12+) |
| 2FA | pyotp (TOTP) |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## 3. Modele de donnees

7 tables : `platforms`, `users_auth`, `sessions`, `refresh_tokens`, `oauth_providers`, `login_history`, `verification_tokens`.

Convention : `user_id` = `users_auth.id` = champ `sub` du JWT.

## 4. Endpoints (30+)

Base URL : `/api/v1`
Documentation interactive : `/api/v1/docs/` (Swagger) ou `/api/v1/redoc/`

### Health
- `GET /auth/health` - Etat du service

### Inscription
- `POST /auth/register` - Inscription email ou telephone
- `POST /auth/verify-email` - Verification email
- `POST /auth/verify-otp` - Verification OTP

### Connexion
- `POST /auth/login` - Email + mot de passe
- `POST /auth/login/phone` - OTP SMS
- `POST /auth/login/magic-link` - Magic link
- `GET /auth/magic-link/callback` - Callback magic link

### OAuth
- `GET /auth/oauth/google` et `/callback` - Google
- `GET /auth/oauth/facebook` et `/callback` - Facebook

### Securite
- `POST /auth/forgot-password` - Lien reset
- `POST /auth/reset-password` - Reset via token
- `PUT /auth/change-password` - Changement

### 2FA
- `POST /auth/2fa/enable` - Activer
- `POST /auth/2fa/confirm` - Confirmer
- `POST /auth/2fa/verify` - Challenge login
- `POST /auth/2fa/disable` - Desactiver

### Sessions
- `POST /auth/refresh` - Rotation (cookie HttpOnly)
- `POST /auth/logout` - Deconnexion
- `GET /auth/sessions` - Sessions actives
- `DELETE /auth/sessions/{id}` - Revoquer
- `GET /auth/verify-token` - Validation JWT (S2S)
- `POST /auth/token/exchange` - Cookie vers Bearer

### Profil
- `GET /auth/me` - Identite pure
- `GET /auth/login-history` - Historique
- `GET /auth/stats/{userId}` - Statistiques

### Administration
- `POST /auth/admin/block/{id}` - Bloquer
- `POST /auth/admin/unblock/{id}` - Debloquer
- `POST /auth/account/deactivate` - Self deactivate
- `POST /auth/admin/deactivate/{id}` - S2S deactivate
- `DELETE /auth/admin/purge/{id}` - Purge RGPD

### Plateformes
- `POST /auth/platforms` - Creer
- `GET /auth/platforms` - Lister
- `PUT /auth/platforms/{id}` - Modifier
- `DELETE /auth/platforms/{id}` - Desactiver

### S2S
- `POST /auth/s2s/token` - Token inter-services
- `POST /auth/s2s/introspect` - Valider token S2S

## 5. Securite

- JWT RS256 (access 15min, refresh 7j cookie HttpOnly)
- Refresh token rotation FIFO (max 5)
- Rate limiting Redis sliding window
- Brute force : blocage apres 5 tentatives (15 min)
- CSRF : SameSite=Lax + Origin + X-Requested-With
- bcrypt cost 12+

## 6. Contrats inter-services

### Auth vers Notification
- Envoi emails/SMS : verification, reset, magic link, OTP
- Transport : HTTP POST sync, timeout 5s, 3x retry

### Auth vers Users
- Provisioning : `POST /api/v1/users` apres inscription
- Sync status : `POST /api/v1/users/status-sync` (deactivation)
- Sync email/phone : `POST /api/v1/users/sync`

## 7. Variables d'environnement

Voir `.env.example` pour la liste complete.

## 8. Port

Service : **7000**

---

*AG Technologies - Auth Service CDC v1.0 - Confidentiel*

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\docker-compose.yml =====
`
services:
  # â”€â”€ PostgreSQL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  db:
    image: postgres:15-alpine
    container_name: agt_auth_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: agt_auth_db
      POSTGRES_USER: agt_user
      POSTGRES_PASSWORD: agt_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agt_user -d agt_auth_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # â”€â”€ Redis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  redis:
    image: redis:7-alpine
    container_name: agt_auth_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # â”€â”€ Auth Service (production) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  auth:
    build:
      context: .
      target: production
    container_name: agt_auth_service
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://agt_user:agt_password@db:5432/agt_auth_db
      REDIS_URL: redis://redis:6379/0
      JWT_PRIVATE_KEY_PATH: /app/keys/private.pem
      JWT_PUBLIC_KEY_PATH: /app/keys/public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7000:7000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7000/api/v1/auth/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # â”€â”€ Auth Service (dev â€” hot reload) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  auth-dev:
    build:
      context: .
      target: builder
    container_name: agt_auth_dev
    restart: unless-stopped
    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py runserver 0.0.0.0:7000"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://agt_user:agt_password@db:5432/agt_auth_db
      REDIS_URL: redis://redis:6379/0
      DEBUG: "True"
      JWT_PRIVATE_KEY_PATH: /app/keys/private.pem
      JWT_PUBLIC_KEY_PATH: /app/keys/public.pem
      DJANGO_SETTINGS_MODULE: config.settings
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7000:7000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles:
      - dev

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\Dockerfile =====
`
# â”€â”€ Builder â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# â”€â”€ Production â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7000", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\manage.py =====
`
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\README.md =====
`
# AGT Auth Service - v1.0

Service d'authentification centralise de l'ecosysteme AG Technologies.

## Stack

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.11+ |
| Framework | Django 5.x + DRF |
| Base de donnees | PostgreSQL 15+ |
| Cache | Redis 7+ |
| JWT | RS256 (PyJWT) |
| Hashing | bcrypt (cost 12+) |
| 2FA | pyotp (TOTP) |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## Prerequisites

- Docker 24+ et Docker Compose v2
- OpenSSL (optionnel sur Windows, le script gere l'absence)

## Demarrage rapide

### Linux / macOS

```bash
bash scripts/setup.sh
```

### Windows (PowerShell)

```powershell
# 1. Ouvrir Docker Desktop et attendre qu'il soit pret (icone verte)

# 2. Autoriser l'execution des scripts (une seule fois par session)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Lancer le setup
.\scripts\setup.ps1
```

> **Note Windows** : Si OpenSSL n'est pas installe, generez les cles manuellement :
> ```powershell
> mkdir keys
> docker run --rm -v "${PWD}\keys:/keys" alpine/openssl genrsa -out /keys/private.pem 2048
> docker run --rm -v "${PWD}\keys:/keys" alpine/openssl rsa -in /keys/private.pem -pubout -out /keys/public.pem
> ```

### Demarrage manuel (tous OS)

```bash
cp .env.example .env
mkdir -p keys
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem
docker compose up -d --build
docker compose exec auth python manage.py migrate --noinput
curl http://localhost:7000/api/v1/auth/health
```

## Documentation API (Swagger)

Une fois le service demarre :

| URL | Description |
|-----|-------------|
| http://localhost:7000/api/v1/docs/ | Swagger UI (interactif) |
| http://localhost:7000/api/v1/redoc/ | ReDoc (lecture) |
| http://localhost:7000/api/v1/schema/ | Schema OpenAPI 3.0 (JSON) |

## Mode developpement (hot reload)

```bash
docker compose --profile dev up auth-dev
```

## Endpoints (30+)

Base URL : `http://localhost:7000/api/v1`

| Methode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/auth/health` | - | Etat du service |
| POST | `/auth/register` | X-Platform-Id | Inscription email ou telephone |
| POST | `/auth/verify-email` | - | Verification email via token |
| POST | `/auth/verify-otp` | - | Verification OTP telephone |
| POST | `/auth/login` | - | Connexion email + mot de passe |
| POST | `/auth/login/phone` | - | Demande OTP SMS |
| POST | `/auth/login/magic-link` | - | Envoi magic link |
| GET | `/auth/magic-link/callback` | - | Callback magic link |
| GET | `/auth/oauth/google` | - | Initier OAuth Google |
| GET | `/auth/oauth/google/callback` | - | Callback Google |
| GET | `/auth/oauth/facebook` | - | Initier OAuth Facebook |
| GET | `/auth/oauth/facebook/callback` | - | Callback Facebook |
| POST | `/auth/forgot-password` | - | Envoi lien reset |
| POST | `/auth/reset-password` | - | Reset via token |
| PUT | `/auth/change-password` | Bearer | Changement mot de passe |
| POST | `/auth/2fa/enable` | Bearer | Activer 2FA |
| POST | `/auth/2fa/confirm` | Bearer | Confirmer activation 2FA |
| POST | `/auth/2fa/verify` | - | Challenge 2FA au login |
| POST | `/auth/2fa/disable` | Bearer | Desactiver 2FA |
| POST | `/auth/refresh` | Cookie | Rotation refresh token |
| POST | `/auth/logout` | Bearer | Deconnexion |
| GET | `/auth/sessions` | Bearer | Sessions actives |
| DELETE | `/auth/sessions/{id}` | Bearer | Revoquer session |
| GET | `/auth/verify-token` | Bearer | Validation JWT (inter-services) |
| POST | `/auth/token/exchange` | Cookie | Cookie vers Bearer |
| GET | `/auth/me` | Bearer | Profil identite |
| GET | `/auth/login-history` | Bearer | Historique connexions |
| GET | `/auth/stats/{userId}` | Bearer | Statistiques |
| POST | `/auth/admin/block/{userId}` | Admin Key | Bloquer utilisateur |
| POST | `/auth/admin/unblock/{userId}` | Admin Key | Debloquer |
| POST | `/auth/account/deactivate` | Bearer | Desactiver son compte |
| POST | `/auth/admin/deactivate/{id}` | Admin Key | Desactivation S2S |
| DELETE | `/auth/admin/purge/{id}` | Admin Key | Purge RGPD |
| POST | `/auth/platforms` | Admin Key | Creer plateforme |
| GET | `/auth/platforms` | Admin Key | Lister plateformes |
| PUT | `/auth/platforms/{id}` | Admin Key | Modifier plateforme |
| DELETE | `/auth/platforms/{id}` | Admin Key | Desactiver plateforme |
| POST | `/auth/s2s/token` | - | Token inter-services |
| POST | `/auth/s2s/introspect` | Bearer | Valider token S2S |

## Tests

```bash
docker compose exec auth python -m pytest -v
```

## Cahier des charges

Voir [CDC_v1.0.md](./CDC_v1.0.md) pour le cahier des charges technique complet.

## Dependances inter-services

| Service | Direction | Usage |
|---------|-----------|-------|
| **Notification** (7002) | Auth vers Notif | Envoi emails/SMS (verification, reset, magic link, OTP) |
| **Users** (7001) | Auth vers Users | Provisioning profil, sync email/phone, sync status |

## Variables d'environnement

Voir `.env.example` pour la liste complete avec descriptions.

---

*AG Technologies - Auth Service v1.0 - Confidentiel*

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\requirements.txt =====
`
# Framework
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1

# Base de donnÃ©es
psycopg2-binary==2.9.9
dj-database-url==2.1.0

# Cache / Sessions
django-redis==5.4.0
redis==5.0.4

# JWT
PyJWT==2.8.0
cryptography==42.0.5

# Hashing
bcrypt==4.1.3

# 2FA / TOTP
pyotp==2.9.0
qrcode==7.4.2
Pillow==10.3.0

# API Documentation (Swagger/OpenAPI 3.0)
drf-spectacular==0.27.2

# Validation & Utilities
phonenumbers==8.13.37
python-decouple==3.8

# Logging
python-json-logger==2.0.7

# HTTP client (appels inter-services)
httpx==0.27.0

# Serveur WSGI production
gunicorn==22.0.0

# Tests
pytest==8.2.0
pytest-django==4.8.0
factory-boy==3.3.0
faker==25.0.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\authentication.py =====
`
"""
AGT Auth Service v1.0 â€” Authentification JWT pour DRF + Admin API Key.
"""
import hmac
import logging

import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.authentication.models import Session, UserAuth
from apps.authentication.services import JWTService

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ", 1)[1]
        return self._validate_token(token)

    def _validate_token(self, token: str):
        cache_key = f"jwt_valid:{token[:32]}"
        cached = cache.get(cache_key)
        if cached == "invalid":
            raise AuthenticationFailed("Token invalide.")
        if cached and isinstance(cached, dict):
            try:
                user = UserAuth.objects.get(id=cached["user_id"])
                return user, cached.get("payload", cached)
            except UserAuth.DoesNotExist:
                pass

        try:
            payload = JWTService.decode_token(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_signature"})

        try:
            user = UserAuth.objects.select_related("registration_platform").get(id=payload["sub"])
        except UserAuth.DoesNotExist:
            raise AuthenticationFailed({"valid": False, "reason": "user_not_found"})

        if user.is_blocked:
            raise AuthenticationFailed({"valid": False, "reason": "user_blocked"})
        if user.is_deactivated:
            raise AuthenticationFailed({"valid": False, "reason": "user_deactivated"})

        session_id = payload.get("session_id")
        if session_id:
            try:
                session = Session.objects.select_related("platform").get(id=session_id)
                if not session.is_active or session.is_expired():
                    raise AuthenticationFailed({"valid": False, "reason": "session_revoked"})
                if not session.platform.is_active:
                    raise AuthenticationFailed({"valid": False, "reason": "platform_inactive"})
            except Session.DoesNotExist:
                raise AuthenticationFailed({"valid": False, "reason": "session_revoked"})

        cache.set(cache_key, {"user_id": str(user.id), "payload": payload}, timeout=30)
        return user, payload

    def authenticate_header(self, request):
        return "Bearer"


class AdminAPIKeyAuthentication:
    @staticmethod
    def verify(request) -> bool:
        api_key = request.headers.get("X-Admin-API-Key", "")
        expected = settings.ADMIN_API_KEY
        if not expected or not api_key:
            return False
        return hmac.compare_digest(api_key.encode(), expected.encode())

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\exceptions.py =====
`
"""
AGT Auth Service v1.0 â€” Exception handler DRF custom.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict) and "detail" not in response.data:
            response.data = {"detail": response.data}
        elif isinstance(response.data, list):
            response.data = {"detail": response.data}
    else:
        logger.exception("Unhandled exception", exc_info=exc)
        response = Response(
            {"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Erreur interne du serveur."}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\models.py =====
`
"""
AGT Auth Service v1.0 â€” ModÃ¨les Django
Conforme au MLD du CDC Auth.
Tables : platforms, users_auth, sessions, refresh_tokens, oauth_providers, login_history, verification_tokens
"""
import uuid
import bcrypt

from django.db import models
from django.utils import timezone


class Platform(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    allowed_auth_methods = models.JSONField(default=list)
    allowed_redirect_urls = models.JSONField(default=list)
    client_secret_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platforms"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    def verify_client_secret(self, raw_secret: str) -> bool:
        return bcrypt.checkpw(raw_secret.encode("utf-8"), self.client_secret_hash.encode("utf-8"))

    @staticmethod
    def hash_client_secret(raw_secret: str, rounds: int = 12) -> str:
        return bcrypt.hashpw(raw_secret.encode("utf-8"), bcrypt.gensalt(rounds=rounds)).decode("utf-8")


class AuthMethodChoice(models.TextChoices):
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"
    GOOGLE = "google", "Google"
    FACEBOOK = "facebook", "Facebook"


class UserAuth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    two_fa_enabled = models.BooleanField(default=False)
    two_fa_secret = models.CharField(max_length=255, null=True, blank=True)
    registration_method = models.CharField(max_length=20, choices=AuthMethodChoice.choices)
    registration_platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="registered_users")
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_auth"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
        ]

    def __str__(self):
        return self.email or self.phone or str(self.id)

    def set_password(self, raw_password: str) -> None:
        from django.conf import settings
        rounds = getattr(settings, "BCRYPT_ROUNDS", 12)
        self.password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt(rounds=rounds)).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        if not self.password_hash:
            return False
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def is_locked(self) -> bool:
        if self.locked_until and self.locked_until > timezone.now():
            return True
        if self.locked_until and self.locked_until <= timezone.now():
            self.failed_login_attempts = 0
            self.locked_until = None
            self.save(update_fields=["failed_login_attempts", "locked_until"])
        return False

    def increment_failed_attempts(self) -> None:
        from django.conf import settings
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= getattr(settings, "BRUTE_FORCE_MAX", 5):
            lockout = getattr(settings, "BRUTE_FORCE_LOCKOUT", 900)
            self.locked_until = timezone.now() + timezone.timedelta(seconds=lockout)
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def reset_failed_attempts(self) -> None:
        if self.failed_login_attempts > 0:
            self.failed_login_attempts = 0
            self.locked_until = None
            self.save(update_fields=["failed_login_attempts", "locked_until"])

    @property
    def is_available_for_login(self):
        if self.is_blocked:
            return False, "user_blocked"
        if self.is_deactivated:
            return False, "user_deactivated"
        if self.is_locked():
            return False, "account_locked"
        return True, ""


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="sessions")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="sessions")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "sessions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["expires_at"]),
        ]

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()

    def revoke(self) -> None:
        self.is_active = False
        self.save(update_fields=["is_active"])


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="refresh_tokens")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="refresh_tokens")
    token_hash = models.CharField(max_length=255, unique=True)
    is_revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "refresh_tokens"
        ordering = ["created_at"]
        indexes = [models.Index(fields=["user", "is_revoked"])]

    def revoke(self) -> None:
        self.is_revoked = True
        self.save(update_fields=["is_revoked"])

    def is_expired(self) -> bool:
        return self.expires_at < timezone.now()


class OAuthProvider(models.Model):
    PROVIDER_CHOICES = [("google", "Google"), ("facebook", "Facebook")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="oauth_providers")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_user_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "oauth_providers"
        constraints = [
            models.UniqueConstraint(fields=["user", "provider"], name="unique_user_provider"),
            models.UniqueConstraint(fields=["provider", "provider_user_id"], name="unique_provider_user_id"),
        ]


class LoginHistory(models.Model):
    LOGIN_METHOD_CHOICES = [
        ("email", "Email/Password"), ("phone", "Phone/OTP"),
        ("google", "Google OAuth"), ("facebook", "Facebook OAuth"),
        ("magic_link", "Magic Link"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="login_history")
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="login_history")
    method = models.CharField(max_length=20, choices=LOGIN_METHOD_CHOICES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    success = models.BooleanField()
    failure_reason = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "login_history"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["platform", "created_at"]),
        ]


class VerificationToken(models.Model):
    TOKEN_TYPE_CHOICES = [
        ("email_verification", "Email Verification"),
        ("password_reset", "Password Reset"),
        ("magic_link", "Magic Link"),
        ("phone_otp", "Phone OTP"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name="verification_tokens")
    token_hash = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=30, choices=TOKEN_TYPE_CHOICES)
    payload = models.JSONField(null=True, blank=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "verification_tokens"
        indexes = [models.Index(fields=["type", "expires_at"])]

    @property
    def is_valid(self) -> bool:
        return self.used_at is None and self.expires_at > timezone.now()

    def mark_as_used(self) -> None:
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\pagination.py =====
`
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "page": self.page.number,
            "limit": self.get_page_size(self.request),
            "total": self.page.paginator.count,
        })

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\permissions.py =====
`
"""
AGT Auth Service v1.0 â€” Permissions DRF customisÃ©es.
"""
from rest_framework.permissions import BasePermission
from apps.authentication.authentication import AdminAPIKeyAuthentication


class IsAdminAPIKey(BasePermission):
    message = {"detail": "ClÃ© API admin invalide ou absente.", "code": "unauthorized"}

    def has_permission(self, request, view):
        return AdminAPIKeyAuthentication.verify(request)


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if AdminAPIKeyAuthentication.verify(request):
            return True
        return request.user and request.user.is_authenticated

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\serializers.py =====
`
"""
AGT Auth Service v1.0 â€” Serializers DRF.
"""
from rest_framework import serializers
from apps.authentication.models import UserAuth, Session, LoginHistory, OAuthProvider


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)
    password = serializers.CharField(min_length=8, required=False, write_only=True, allow_null=True)
    method = serializers.ChoiceField(choices=["email", "phone"])

    def validate(self, data):
        method = data.get("method")
        if method == "email":
            if not data.get("email"):
                raise serializers.ValidationError({"email": "Champ obligatoire pour method=email."})
            if not data.get("password"):
                raise serializers.ValidationError({"password": "Champ obligatoire pour method=email."})
        elif method == "phone":
            if not data.get("phone"):
                raise serializers.ValidationError({"phone": "Champ obligatoire pour method=phone."})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    platform_id = serializers.UUIDField()


class LoginPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    platform_id = serializers.UUIDField()


class MagicLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()
    platform_id = serializers.UUIDField()
    redirect_url = serializers.URLField()


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(min_length=4, max_length=8)
    context = serializers.ChoiceField(choices=["registration", "login"])
    platform_id = serializers.UUIDField(required=False)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data["current_password"] == data["new_password"]:
            raise serializers.ValidationError("Le nouveau mot de passe doit Ãªtre diffÃ©rent de l'ancien.")
        return data


class DeactivateAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class TwoFAConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)


class TwoFAVerifySerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)
    temp_token = serializers.CharField()


class TwoFADisableSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)


class SessionResponseSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.slug", read_only=True)
    is_current = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ["id", "platform", "ip_address", "user_agent", "created_at", "is_current"]

    def get_is_current(self, obj):
        current = self.context.get("current_session_id")
        return str(obj.id) == str(current) if current else False


class LoginHistoryResponseSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.slug", read_only=True)

    class Meta:
        model = LoginHistory
        fields = ["id", "method", "platform", "ip_address", "success", "created_at"]


class UserAuthResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = [
            "id", "email", "phone", "email_verified", "phone_verified",
            "two_fa_enabled", "registration_method", "is_blocked",
            "is_deactivated", "created_at",
        ]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\services.py =====
`
"""
AGT Auth Service v1.0 â€” Services : JWT, Token, TOTP, Session, inter-services clients.
"""
import hashlib
import hmac
import secrets
import uuid
import logging
from datetime import timedelta
from typing import Optional

import jwt
import pyotp
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class JWTService:
    @staticmethod
    def generate_access_token(user, platform_id: str, session_id: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(user.id),
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=settings.JWT_ACCESS_TTL)).timestamp()),
            "jti": str(uuid.uuid4()),
            "session_id": str(session_id),
            "platform_id": str(platform_id),
            "email": user.email,
            "email_verified": user.email_verified,
            "two_fa_verified": False,
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_access_token_2fa(user, platform_id: str, session_id: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(user.id),
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=settings.JWT_ACCESS_TTL)).timestamp()),
            "jti": str(uuid.uuid4()),
            "session_id": str(session_id),
            "platform_id": str(platform_id),
            "email": user.email,
            "email_verified": user.email_verified,
            "two_fa_verified": True,
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_temp_token(user_id: str, platform_id: str, session_id: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(user_id), "type": "2fa_challenge",
            "session_id": str(session_id), "platform_id": str(platform_id),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=5)).timestamp()),
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_s2s_token(platform_id: str, platform_name: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(platform_id), "type": "s2s", "service_name": platform_name,
            "iss": settings.JWT_ISSUER, "aud": settings.JWT_AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=1)).timestamp()),
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=["RS256"],
                          audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER)

    @staticmethod
    def decode_token_unverified(token: str) -> dict:
        return jwt.decode(token, options={"verify_signature": False})


class TokenService:
    @staticmethod
    def generate_raw_token(length: int = 64) -> str:
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_otp(digits: int = 6) -> str:
        return str(secrets.randbelow(10 ** digits)).zfill(digits)

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @staticmethod
    def hash_refresh_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @staticmethod
    def constant_time_compare(val1: str, val2: str) -> bool:
        return hmac.compare_digest(val1.encode(), val2.encode())


class TOTPService:
    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()

    @staticmethod
    def get_totp_uri(secret: str, email: str) -> str:
        return pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name="AGT")

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        return pyotp.TOTP(secret).verify(code, valid_window=1)

    @staticmethod
    def encrypt_secret(raw_secret: str) -> str:
        import base64
        return base64.b64encode(raw_secret.encode()).decode()

    @staticmethod
    def decrypt_secret(encrypted_secret: str) -> str:
        import base64
        return base64.b64decode(encrypted_secret.encode()).decode()


class SessionService:
    @staticmethod
    def create_session(user, platform, ip_address: str, user_agent: str = None):
        from apps.authentication.models import Session
        return Session.objects.create(
            user=user, platform=platform, ip_address=ip_address, user_agent=user_agent,
            expires_at=timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TTL),
        )

    @staticmethod
    def create_refresh_token(user, session) -> str:
        from apps.authentication.models import RefreshToken
        max_tokens = getattr(settings, "MAX_REFRESH_TOKENS", 5)
        active_tokens = RefreshToken.objects.filter(user=user, is_revoked=False).order_by("created_at")
        count = active_tokens.count()
        if count >= max_tokens:
            to_revoke = active_tokens[: count - max_tokens + 1]
            RefreshToken.objects.filter(id__in=[t.id for t in to_revoke]).update(is_revoked=True)

        raw_token = TokenService.generate_raw_token()
        token_hash = TokenService.hash_refresh_token(raw_token)
        RefreshToken.objects.create(
            user=user, session=session, token_hash=token_hash,
            expires_at=timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TTL),
        )
        return raw_token

    @staticmethod
    def revoke_all_sessions(user, except_session_id=None) -> int:
        from apps.authentication.models import Session, RefreshToken
        qs = Session.objects.filter(user=user, is_active=True)
        if except_session_id:
            qs = qs.exclude(id=except_session_id)
        session_ids = list(qs.values_list("id", flat=True))
        RefreshToken.objects.filter(session_id__in=session_ids).update(is_revoked=True)
        return qs.update(is_active=False)

    @staticmethod
    def revoke_session(session) -> None:
        from apps.authentication.models import RefreshToken
        RefreshToken.objects.filter(session=session).update(is_revoked=True)
        session.is_active = False
        session.save(update_fields=["is_active"])


class NotificationClient:
    @staticmethod
    def send(notification_type: str, recipient: dict, template: str, data: dict, priority: str = "normal") -> bool:
        import httpx
        url = getattr(settings, "NOTIFICATION_SERVICE_URL", "")
        if not url:
            logger.warning("NOTIFICATION_SERVICE_URL non configurÃ© â€” notification ignorÃ©e.")
            return False
        try:
            resp = httpx.post(f"{url}/notifications/send", json={
                "type": notification_type,
                "recipient": recipient,
                "template": template,
                "data": data,
                "priority": priority,
                "idempotency_key": str(uuid.uuid4()),
            }, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Notification Ã©chouÃ©e: {e}")
            return False


class UsersServiceClient:
    @staticmethod
    def provision_user(auth_user_id: str, email: str = None, phone: str = None, first_name: str = "", last_name: str = "") -> bool:
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            logger.warning("USERS_SERVICE_URL non configurÃ© â€” provisioning ignorÃ©.")
            return False
        try:
            resp = httpx.post(f"{url}/users", json={
                "auth_user_id": auth_user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
            }, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Provisioning Users Ã©chouÃ©: {e}")
            return False

    @staticmethod
    def sync_status(auth_user_id: str, status: str) -> bool:
        """Pousse un changement de statut vers Users (CDC: POST /api/v1/users/status-sync)."""
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return False
        try:
            resp = httpx.post(f"{url}/users/status-sync", json={
                "auth_user_id": auth_user_id,
                "status": status,
            }, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Status sync Users Ã©chouÃ©: {e}")
            return False

    @staticmethod
    def sync_credentials(auth_user_id: str, email: str = None, phone: str = None) -> bool:
        """Pousse un changement email/phone vers Users (CDC: POST /api/v1/users/sync)."""
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return False
        payload = {"auth_user_id": auth_user_id}
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        try:
            resp = httpx.post(f"{url}/users/sync", json=payload, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Credentials sync Users Ã©chouÃ©: {e}")
            return False

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\swagger.py =====
`
"""
AGT Auth Service v1.0 - Annotations Swagger/OpenAPI (drf-spectacular).
Importer et appliquer via @extend_schema sur chaque view.
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


# --- Health ---
health_schema = extend_schema(
    tags=["Health"],
    summary="Health check",
    description="Verifie l'etat du service (DB, Redis). Aucune authentification requise.",
    responses={
        200: {"type": "object", "properties": {
            "status": {"type": "string", "example": "healthy"},
            "database": {"type": "string", "example": "ok"},
            "redis": {"type": "string", "example": "ok"},
            "version": {"type": "string", "example": "1.0.0"},
        }},
        503: {"description": "Service degraded"},
    },
)

# --- Register ---
register_schema = extend_schema(
    tags=["Register"],
    summary="Inscription (email ou telephone)",
    description="Cree un nouveau compte. Header X-Platform-Id obligatoire. Le flux OAuth ne passe pas par cet endpoint.",
    parameters=[OpenApiParameter(name="X-Platform-Id", location=OpenApiParameter.HEADER, required=True, type=str, description="UUID de la plateforme")],
    request={"type": "object", "properties": {
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "string", "example": "+237600000000"},
        "password": {"type": "string", "minLength": 8},
        "method": {"type": "string", "enum": ["email", "phone"]},
    }, "required": ["method"]},
    responses={201: {"description": "Compte cree"}, 400: {"description": "Validation error"}, 409: {"description": "Email/phone deja utilise"}},
)

# --- Login ---
login_schema = extend_schema(
    tags=["Login"],
    summary="Connexion email + mot de passe",
    description="Retourne un access_token JWT. Le refresh_token est pose en cookie HttpOnly.",
    responses={200: {"description": "Connexion reussie"}, 401: {"description": "Identifiants invalides"}, 403: {"description": "Compte bloque/desactive"}, 429: {"description": "Rate limited"}},
)

login_phone_schema = extend_schema(
    tags=["Login"],
    summary="Demande OTP par SMS",
    description="Envoie un code OTP au numero. Le client soumet ensuite via POST /auth/verify-otp.",
)

magic_link_schema = extend_schema(
    tags=["Login"],
    summary="Envoi magic link par email",
    description="Envoie un lien de connexion. Le clic redirige vers le callback qui pose les cookies.",
)

magic_link_callback_schema = extend_schema(
    tags=["Login"],
    summary="Callback magic link",
    description="Traite le clic sur le magic link. Pose les tokens en cookies HttpOnly et redirige.",
    parameters=[OpenApiParameter(name="token", location=OpenApiParameter.QUERY, required=True, type=str)],
    responses={302: {"description": "Redirect avec cookies"}, 400: {"description": "Token invalide"}, 403: {"description": "Utilisateur bloque"}},
)

# --- Verify ---
verify_email_schema = extend_schema(
    tags=["Register"],
    summary="Verification email via token",
)

verify_otp_schema = extend_schema(
    tags=["Register"],
    summary="Verification OTP telephone",
    description="Contexte 'registration' = verification. Contexte 'login' = connexion avec tokens retournes.",
)

# --- Password ---
forgot_password_schema = extend_schema(
    tags=["Password"],
    summary="Envoi lien de reinitialisation",
    description="Reponse generique meme si l'email n'existe pas (securite).",
)

reset_password_schema = extend_schema(
    tags=["Password"],
    summary="Reinitialisation via token",
    description="Reinitialise le mot de passe et revoque toutes les sessions.",
)

change_password_schema = extend_schema(
    tags=["Password"],
    summary="Changement avec ancien mot de passe",
    description="Revoque toutes les sessions sauf la courante.",
)

# --- 2FA ---
twofa_enable_schema = extend_schema(tags=["2FA"], summary="Activer 2FA - generer secret + QR code")
twofa_confirm_schema = extend_schema(tags=["2FA"], summary="Confirmer activation 2FA")
twofa_verify_schema = extend_schema(tags=["2FA"], summary="Challenge 2FA au login", description="Appele quand requires_2fa=true. Echange le temp_token + code contre un access_token.")
twofa_disable_schema = extend_schema(tags=["2FA"], summary="Desactiver 2FA")

# --- Sessions ---
refresh_schema = extend_schema(
    tags=["Sessions"],
    summary="Rotation refresh token",
    description="Le refresh token est lu depuis le cookie HttpOnly. Un nouveau est emis (rotation).",
)

logout_schema = extend_schema(tags=["Sessions"], summary="Deconnexion", description="Revoque la session courante et supprime le cookie refresh_token.")

session_list_schema = extend_schema(tags=["Sessions"], summary="Lister sessions actives")
session_revoke_schema = extend_schema(tags=["Sessions"], summary="Revoquer une session")

verify_token_schema = extend_schema(
    tags=["Sessions"],
    summary="Validation JWT (inter-services)",
    description="Endpoint interne. Effectue 6 verifications : signature, expiration, blocked, deactivated, platform active, session active.",
    responses={200: {"description": "Token valide"}, 401: {"description": "Token invalide avec raison"}},
)

token_exchange_schema = extend_schema(
    tags=["Sessions"],
    summary="Echange cookie vers Bearer",
    description="Apres callback OAuth/magic-link. Lit le cookie access_token et le retourne en JSON.",
)

# --- Profile ---
me_schema = extend_schema(tags=["Profile"], summary="Profil identite (sans roles)", description="Retourne l'identite pure. Les roles sont dans le Service Users.")
login_history_schema = extend_schema(tags=["Profile"], summary="Historique des connexions")
user_stats_schema = extend_schema(tags=["Profile"], summary="Statistiques utilisateur")

# --- Admin ---
block_schema = extend_schema(tags=["Admin"], summary="Bloquer un utilisateur", description="Revoque toutes les sessions. Ne modifie pas le statut Users.")
unblock_schema = extend_schema(tags=["Admin"], summary="Debloquer un utilisateur")
deactivate_self_schema = extend_schema(tags=["Admin"], summary="Desactiver son propre compte", description="Mot de passe requis. Propage status-sync vers Users.")
deactivate_admin_schema = extend_schema(tags=["Admin"], summary="Desactivation S2S (inter-service)", description="Appele par Users pour soft delete global sans mot de passe.")
purge_schema = extend_schema(tags=["Admin"], summary="Purge RGPD", description="Suppression physique irreversible. Transactionnel.")

# --- OAuth ---
oauth_google_init_schema = extend_schema(tags=["OAuth"], summary="Initier OAuth Google", parameters=[
    OpenApiParameter(name="platform_id", location=OpenApiParameter.QUERY, type=str),
    OpenApiParameter(name="redirect_uri", location=OpenApiParameter.QUERY, type=str),
])
oauth_google_callback_schema = extend_schema(tags=["OAuth"], summary="Callback OAuth Google")
oauth_facebook_init_schema = extend_schema(tags=["OAuth"], summary="Initier OAuth Facebook")
oauth_facebook_callback_schema = extend_schema(tags=["OAuth"], summary="Callback OAuth Facebook")

# --- Platforms ---
platform_list_create_schema = extend_schema(tags=["Platforms"], summary="Creer ou lister les plateformes")
platform_detail_schema = extend_schema(tags=["Platforms"], summary="Modifier ou desactiver une plateforme")

# --- S2S ---
s2s_token_schema = extend_schema(tags=["S2S"], summary="Generer token S2S", description="Flux Client Credentials. Retourne un JWT S2S valide 1h.")
s2s_introspect_schema = extend_schema(tags=["S2S"], summary="Valider token S2S", description="Permet a un service de verifier la validite d'un token S2S plateforme.")

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\urls.py =====
`
"""
AGT Auth Service v1.0 â€” URLs
"""
from django.urls import path
from apps.authentication.views_auth import (
    HealthCheckView, RegisterView, VerifyEmailView, VerifyOTPView,
    LoginView, LoginPhoneView, MagicLinkRequestView, MagicLinkCallbackView,
)
from apps.authentication.views_sessions import (
    RefreshTokenView, LogoutView, SessionListView, SessionRevokeView,
    VerifyTokenView, TokenExchangeView, ForgotPasswordView, ResetPasswordView,
    ChangePasswordView, TwoFAEnableView, TwoFAConfirmView, TwoFAVerifyView,
    TwoFADisableView, MeView, LoginHistoryView, UserStatsView,
)
from apps.authentication.views_admin import (
    AdminBlockUserView, AdminUnblockUserView, AccountDeactivateView,
    AdminDeactivateUserView, AdminPurgeUserView,
    OAuthGoogleInitView, OAuthGoogleCallbackView,
    OAuthFacebookInitView, OAuthFacebookCallbackView,
    S2STokenView, S2SIntrospectView,
)

urlpatterns = [
    # Health
    path("auth/health", HealthCheckView.as_view(), name="auth-health"),

    # Register & Verify
    path("auth/register", RegisterView.as_view(), name="auth-register"),
    path("auth/verify-email", VerifyEmailView.as_view(), name="auth-verify-email"),
    path("auth/verify-otp", VerifyOTPView.as_view(), name="auth-verify-otp"),

    # Login
    path("auth/login", LoginView.as_view(), name="auth-login"),
    path("auth/login/phone", LoginPhoneView.as_view(), name="auth-login-phone"),
    path("auth/login/magic-link", MagicLinkRequestView.as_view(), name="auth-magic-link"),
    path("auth/magic-link/callback", MagicLinkCallbackView.as_view(), name="auth-magic-link-callback"),

    # OAuth
    path("auth/oauth/google", OAuthGoogleInitView.as_view(), name="auth-oauth-google"),
    path("auth/oauth/google/callback", OAuthGoogleCallbackView.as_view(), name="auth-oauth-google-callback"),
    path("auth/oauth/facebook", OAuthFacebookInitView.as_view(), name="auth-oauth-facebook"),
    path("auth/oauth/facebook/callback", OAuthFacebookCallbackView.as_view(), name="auth-oauth-facebook-callback"),

    # Password
    path("auth/forgot-password", ForgotPasswordView.as_view(), name="auth-forgot-password"),
    path("auth/reset-password", ResetPasswordView.as_view(), name="auth-reset-password"),
    path("auth/change-password", ChangePasswordView.as_view(), name="auth-change-password"),

    # 2FA
    path("auth/2fa/enable", TwoFAEnableView.as_view(), name="auth-2fa-enable"),
    path("auth/2fa/confirm", TwoFAConfirmView.as_view(), name="auth-2fa-confirm"),
    path("auth/2fa/verify", TwoFAVerifyView.as_view(), name="auth-2fa-verify"),
    path("auth/2fa/disable", TwoFADisableView.as_view(), name="auth-2fa-disable"),

    # Sessions & Tokens
    path("auth/refresh", RefreshTokenView.as_view(), name="auth-refresh"),
    path("auth/logout", LogoutView.as_view(), name="auth-logout"),
    path("auth/sessions", SessionListView.as_view(), name="auth-sessions"),
    path("auth/sessions/<uuid:session_id>", SessionRevokeView.as_view(), name="auth-session-revoke"),
    path("auth/verify-token", VerifyTokenView.as_view(), name="auth-verify-token"),
    path("auth/token/exchange", TokenExchangeView.as_view(), name="auth-token-exchange"),

    # Profile & Audit
    path("auth/me", MeView.as_view(), name="auth-me"),
    path("auth/login-history", LoginHistoryView.as_view(), name="auth-login-history"),
    path("auth/stats/<uuid:user_id>", UserStatsView.as_view(), name="auth-stats"),

    # Administration
    path("auth/admin/block/<uuid:user_id>", AdminBlockUserView.as_view(), name="auth-admin-block"),
    path("auth/admin/unblock/<uuid:user_id>", AdminUnblockUserView.as_view(), name="auth-admin-unblock"),
    path("auth/account/deactivate", AccountDeactivateView.as_view(), name="auth-account-deactivate"),
    path("auth/admin/deactivate/<uuid:auth_user_id>", AdminDeactivateUserView.as_view(), name="auth-admin-deactivate"),
    path("auth/admin/purge/<uuid:auth_user_id>", AdminPurgeUserView.as_view(), name="auth-admin-purge"),

    # S2S
    path("auth/s2s/token", S2STokenView.as_view(), name="auth-s2s-token"),
    path("auth/s2s/introspect", S2SIntrospectView.as_view(), name="auth-s2s-introspect"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\utils.py =====
`
"""
AGT Auth Service v1.0 â€” Utilitaires : extraction IP, gestion cookies sÃ©curisÃ©s.
"""
from django.conf import settings


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def set_refresh_cookie(response, raw_refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token", value=raw_refresh_token,
        max_age=settings.JWT_REFRESH_TTL, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/api/v1/auth/refresh",
    )


def set_access_cookie(response, access_token: str) -> None:
    response.set_cookie(
        key="access_token", value=access_token,
        max_age=settings.JWT_ACCESS_TTL, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/",
    )


def clear_refresh_cookie(response) -> None:
    response.set_cookie(
        key="refresh_token", value="", max_age=0, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/api/v1/auth/refresh",
    )


def clear_access_cookie(response) -> None:
    response.set_cookie(
        key="access_token", value="", max_age=0, httponly=True,
        secure=getattr(settings, "COOKIE_SECURE", False),
        samesite=getattr(settings, "COOKIE_SAMESITE", "Lax"),
        path="/",
    )

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\views_admin.py =====
`
"""
AGT Auth Service v1.0 â€” Views : Administration, OAuth, S2S tokens.
"""
import logging
import secrets as sec

import httpx
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import redirect as django_redirect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import (
    UserAuth, Session, RefreshToken, OAuthProvider,
    LoginHistory, VerificationToken, Platform,
)
from apps.authentication.permissions import IsAdminAPIKey
from apps.authentication.serializers import DeactivateAccountSerializer
from apps.authentication.services import (
    JWTService, TokenService, SessionService, UsersServiceClient,
)
from apps.authentication.utils import get_client_ip, set_refresh_cookie, set_access_cookie
from apps.authentication.swagger import (
    block_schema, unblock_schema, deactivate_self_schema, deactivate_admin_schema,
    purge_schema, oauth_google_init_schema, oauth_google_callback_schema,
    oauth_facebook_init_schema, oauth_facebook_callback_schema,
    s2s_token_schema, s2s_introspect_schema,
)

logger = logging.getLogger(__name__)


# â”€â”€â”€ Block / Unblock â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


@block_schema
class AdminBlockUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request, user_id):
        try:
            user = UserAuth.objects.get(id=user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = True
        user.save(update_fields=["is_blocked", "updated_at"])
        SessionService.revoke_all_sessions(user)
        return Response({"message": "User blocked", "user_id": str(user.id), "is_blocked": True})



@unblock_schema
class AdminUnblockUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request, user_id):
        try:
            user = UserAuth.objects.get(id=user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = False
        user.save(update_fields=["is_blocked", "updated_at"])
        return Response({"message": "User unblocked", "user_id": str(user.id), "is_blocked": False})


# â”€â”€â”€ Deactivate â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


@deactivate_self_schema
class AccountDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeactivateAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(serializer.validated_data["password"]):
            return Response({"detail": "Mot de passe incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_deactivated = True
        user.save(update_fields=["is_deactivated", "updated_at"])
        SessionService.revoke_all_sessions(user)

        # Propager status-sync vers Users (CDC: POST /api/v1/users/status-sync)
        UsersServiceClient.sync_status(str(user.id), "inactive")

        return Response({"message": "Account deactivated", "is_deactivated": True})



@deactivate_admin_schema
class AdminDeactivateUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request, auth_user_id):
        try:
            user = UserAuth.objects.get(id=auth_user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.is_deactivated = True
        user.save(update_fields=["is_deactivated", "updated_at"])
        SessionService.revoke_all_sessions(user)

        UsersServiceClient.sync_status(str(user.id), "inactive")

        return Response({"message": "User deactivated", "user_id": str(user.id), "is_deactivated": True})


# â”€â”€â”€ Purge RGPD â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


@purge_schema
class AdminPurgeUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def delete(self, request, auth_user_id):
        try:
            user = UserAuth.objects.get(id=auth_user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                VerificationToken.objects.filter(user=user).delete()
                LoginHistory.objects.filter(user=user).delete()
                OAuthProvider.objects.filter(user=user).delete()
                RefreshToken.objects.filter(user=user).delete()
                Session.objects.filter(user=user).delete()
                user.delete()
        except Exception as e:
            logger.error(f"Purge partielle Ã©chouÃ©e pour {auth_user_id}: {e}")
            return Response({"detail": "Ã‰chec de purge."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "User purged", "user_id": str(auth_user_id), "purged": True})


# â”€â”€â”€ OAuth Google â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


@oauth_google_init_schema
class OAuthGoogleInitView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        platform_id = request.GET.get("platform_id", "")
        redirect_uri = request.GET.get("redirect_uri", settings.GOOGLE_REDIRECT_URI)
        state = sec.token_urlsafe(32)

        cache.set(f"oauth_state:{state}", {"platform_id": platform_id, "redirect_uri": redirect_uri}, timeout=600)

        params = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            f"&response_type=code"
            f"&scope=openid+email+profile"
            f"&state={state}"
            f"&access_type=offline"
        )
        return django_redirect(params)



@oauth_google_callback_schema
class OAuthGoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")

        cached_state = cache.get(f"oauth_state:{state}")
        if not cached_state:
            return Response({"detail": "State OAuth invalide."}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"oauth_state:{state}")
        platform_id = cached_state.get("platform_id")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Ã‰changer le code contre un token Google
        try:
            token_resp = httpx.post("https://oauth2.googleapis.com/token", data={
                "code": code, "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }, timeout=10.0)
            google_token = token_resp.json().get("access_token")
        except Exception as e:
            logger.error(f"Google token exchange failed: {e}")
            return Response({"detail": "Erreur OAuth Google."}, status=status.HTTP_502_BAD_GATEWAY)

        # RÃ©cupÃ©rer le profil Google
        try:
            profile_resp = httpx.get("https://www.googleapis.com/oauth2/v2/userinfo",
                                     headers={"Authorization": f"Bearer {google_token}"}, timeout=10.0)
            profile = profile_resp.json()
            google_id = profile.get("id")
            google_email = profile.get("email")
        except Exception as e:
            logger.error(f"Google profile fetch failed: {e}")
            return Response({"detail": "Erreur profil Google."}, status=status.HTTP_502_BAD_GATEWAY)

        # Trouver ou crÃ©er l'utilisateur
        try:
            oauth = OAuthProvider.objects.select_related("user").get(provider="google", provider_user_id=google_id)
            user = oauth.user
        except OAuthProvider.DoesNotExist:
            user = UserAuth.objects.filter(email=google_email).first()
            if not user:
                user = UserAuth.objects.create(
                    email=google_email, email_verified=True,
                    registration_method="google", registration_platform=platform,
                )
                UsersServiceClient.provision_user(str(user.id), email=google_email)
            OAuthProvider.objects.create(user=user, provider="google", provider_user_id=google_id, email=google_email)

        available, reason = user.is_available_for_login
        if not available:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

        LoginHistory.objects.create(user=user, platform=platform, method="google", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        final_redirect = cached_state.get("redirect_uri", "/")
        response = django_redirect(final_redirect)
        set_access_cookie(response, access_token)
        set_refresh_cookie(response, raw_refresh)
        return response


# â”€â”€â”€ OAuth Facebook â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


@oauth_facebook_init_schema
class OAuthFacebookInitView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        platform_id = request.GET.get("platform_id", "")
        redirect_uri = request.GET.get("redirect_uri", settings.FACEBOOK_REDIRECT_URI)
        state = sec.token_urlsafe(32)
        cache.set(f"oauth_state:{state}", {"platform_id": platform_id, "redirect_uri": redirect_uri}, timeout=600)

        params = (f"https://www.facebook.com/v19.0/dialog/oauth"
                  f"?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
                  f"&scope=email&state={state}")
        return django_redirect(params)



@oauth_facebook_callback_schema
class OAuthFacebookCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")
        cached_state = cache.get(f"oauth_state:{state}")
        if not cached_state:
            return Response({"detail": "State OAuth invalide."}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"oauth_state:{state}")
        platform_id = cached_state.get("platform_id")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_resp = httpx.get(
                f"https://graph.facebook.com/v19.0/oauth/access_token"
                f"?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
                f"&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}", timeout=10.0)
            fb_token = token_resp.json().get("access_token")
            profile_resp = httpx.get(f"https://graph.facebook.com/me?fields=id,email&access_token={fb_token}", timeout=10.0)
            profile = profile_resp.json()
            fb_id = profile.get("id")
            fb_email = profile.get("email")
        except Exception as e:
            logger.error(f"Facebook OAuth failed: {e}")
            return Response({"detail": "Erreur OAuth Facebook."}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            oauth = OAuthProvider.objects.select_related("user").get(provider="facebook", provider_user_id=fb_id)
            user = oauth.user
        except OAuthProvider.DoesNotExist:
            user = UserAuth.objects.filter(email=fb_email).first() if fb_email else None
            if not user:
                user = UserAuth.objects.create(
                    email=fb_email, email_verified=bool(fb_email),
                    registration_method="facebook", registration_platform=platform,
                )
                UsersServiceClient.provision_user(str(user.id), email=fb_email)
            OAuthProvider.objects.create(user=user, provider="facebook", provider_user_id=fb_id, email=fb_email)

        available, reason = user.is_available_for_login
        if not available:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

        LoginHistory.objects.create(user=user, platform=platform, method="facebook", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        response = django_redirect(cached_state.get("redirect_uri", "/"))
        set_access_cookie(response, access_token)
        set_refresh_cookie(response, raw_refresh)
        return response


# â”€â”€â”€ S2S Tokens â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


@s2s_token_schema
class S2STokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        client_id = request.data.get("client_id")
        client_secret = request.data.get("client_secret")
        if not client_id or not client_secret:
            return Response({"detail": "client_id et client_secret requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            platform = Platform.objects.get(id=client_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        if not platform.verify_client_secret(client_secret):
            return Response({"detail": "Secret invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        token = JWTService.generate_s2s_token(str(platform.id), platform.name)
        return Response({"access_token": token, "token_type": "Bearer", "expires_in": 3600, "service_name": platform.name})



@s2s_introspect_schema
class S2SIntrospectView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "token requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = JWTService.decode_token(token)
            if payload.get("type") != "s2s":
                return Response({"active": False})
            return Response({"active": True, "client_id": payload["sub"], "service_name": payload.get("service_name"), "exp": payload["exp"]})
        except Exception:
            return Response({"active": False})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\views_auth.py =====
`
"""
AGT Auth Service v1.0 - Views : Health, Register, Verify, Login, MagicLink.
"""
import logging
from datetime import timedelta

from django.conf import settings
from django.shortcuts import redirect as django_redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import Platform, UserAuth, VerificationToken, LoginHistory
from apps.authentication.serializers import (
    RegisterSerializer, VerifyEmailSerializer, VerifyOTPSerializer,
    LoginSerializer, LoginPhoneSerializer, MagicLinkSerializer,
)
from apps.authentication.services import (
    JWTService, TokenService, SessionService, NotificationClient, UsersServiceClient,
)
from apps.authentication.utils import get_client_ip, set_refresh_cookie, set_access_cookie
from apps.authentication.swagger import (
    health_schema, register_schema, verify_email_schema, verify_otp_schema,
    login_schema, login_phone_schema, magic_link_schema, magic_link_callback_schema,
)

logger = logging.getLogger(__name__)



@health_schema
class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        db_ok = redis_ok = True
        try:
            from django.db import connection
            connection.ensure_connection()
        except Exception:
            db_ok = False
        try:
            from django.core.cache import cache
            cache.set("health_ping", "pong", 5)
            redis_ok = cache.get("health_ping") == "pong"
        except Exception:
            redis_ok = False

        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            "status": "healthy" if db_ok and redis_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "version": "1.0.0",
        }, status=code)



@register_schema
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        platform_id = request.headers.get("X-Platform-Id")
        if not platform_id:
            return Response({"detail": "Header X-Platform-Id requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide ou inactive."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        method = data["method"]

        # VÃ©rifier doublon
        if method == "email" and UserAuth.objects.filter(email=data["email"]).exists():
            return Response({"detail": "Email dÃ©jÃ  utilisÃ©."}, status=status.HTTP_409_CONFLICT)
        if method == "phone" and UserAuth.objects.filter(phone=data["phone"]).exists():
            return Response({"detail": "TÃ©lÃ©phone dÃ©jÃ  utilisÃ©."}, status=status.HTTP_409_CONFLICT)

        # VÃ©rifier mÃ©thode autorisÃ©e
        if method not in platform.allowed_auth_methods:
            return Response({"detail": f"MÃ©thode '{method}' non autorisÃ©e sur cette plateforme."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserAuth(registration_method=method, registration_platform=platform)

        if method == "email":
            user.email = data["email"]
            user.set_password(data["password"])
            user.save()

            # Token de vÃ©rification email
            raw_token = TokenService.generate_raw_token()
            VerificationToken.objects.create(
                user=user, token_hash=TokenService.hash_token(raw_token),
                type="email_verification",
                expires_at=timezone.now() + timedelta(hours=1),
            )

            NotificationClient.send(
                notification_type="email_verification",
                recipient={"email": user.email, "phone": None},
                template="auth_verify_email",
                data={"verification_url": f"{request.scheme}://{request.get_host()}/api/v1/auth/verify-email?token={raw_token}", "expires_in_minutes": 60, "platform_name": platform.name},
                priority="high",
            )

            # Provisioning Users
            UsersServiceClient.provision_user(str(user.id), email=user.email)

            return Response({
                "id": str(user.id), "email": user.email, "email_verified": False,
                "registration_method": "email", "registration_platform_id": str(platform.id),
                "message": "Verification email sent",
            }, status=status.HTTP_201_CREATED)

        elif method == "phone":
            user.phone = data["phone"]
            user.save()

            otp = TokenService.generate_otp()
            VerificationToken.objects.create(
                user=user, token_hash=TokenService.hash_token(otp),
                type="phone_otp", payload={"context": "registration"},
                expires_at=timezone.now() + timedelta(seconds=settings.OTP_TTL),
            )

            NotificationClient.send(
                notification_type="phone_otp",
                recipient={"email": None, "phone": user.phone},
                template="auth_otp_sms",
                data={"otp_code": otp, "expires_in_minutes": settings.OTP_TTL // 60, "platform_name": platform.name},
                priority="critical",
            )

            UsersServiceClient.provision_user(str(user.id), phone=user.phone)

            return Response({
                "id": str(user.id), "phone": user.phone, "phone_verified": False,
                "registration_method": "phone", "registration_platform_id": str(platform.id),
                "message": "OTP sent",
            }, status=status.HTTP_201_CREATED)



@verify_email_schema
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token_hash = TokenService.hash_token(serializer.validated_data["token"])
        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="email_verification")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "Token expirÃ© ou dÃ©jÃ  utilisÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        vtoken.user.email_verified = True
        vtoken.user.save(update_fields=["email_verified", "updated_at"])

        return Response({"message": "Email verified", "email_verified": True})



@verify_otp_schema
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        token_hash = TokenService.hash_token(data["otp_code"])

        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="phone_otp")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "OTP invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "OTP expirÃ© ou dÃ©jÃ  utilisÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        user = vtoken.user

        if data["context"] == "registration":
            user.phone_verified = True
            user.save(update_fields=["phone_verified", "updated_at"])
            return Response({"message": "Phone verified", "phone_verified": True})

        elif data["context"] == "login":
            platform_id = data.get("platform_id")
            try:
                platform = Platform.objects.get(id=platform_id, is_active=True)
            except Platform.DoesNotExist:
                return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

            available, reason = user.is_available_for_login
            if not available:
                return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

            ip = get_client_ip(request)
            session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
            raw_refresh = SessionService.create_refresh_token(user, session)
            access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

            LoginHistory.objects.create(user=user, platform=platform, method="phone", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

            response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
            set_refresh_cookie(response, raw_refresh)
            return response



@login_schema
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            platform = Platform.objects.get(id=data["platform_id"], is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAuth.objects.get(email=data["email"])
        except UserAuth.DoesNotExist:
            return Response({"detail": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        available, reason = user.is_available_for_login
        if not available:
            LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=get_client_ip(request), user_agent=request.headers.get("User-Agent"), success=False, failure_reason=reason)
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(data["password"]):
            user.increment_failed_attempts()
            LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=get_client_ip(request), user_agent=request.headers.get("User-Agent"), success=False, failure_reason="invalid_password")
            return Response({"detail": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        user.reset_failed_attempts()
        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)

        # 2FA check
        if user.two_fa_enabled:
            temp_token = JWTService.generate_temp_token(str(user.id), str(platform.id), str(session.id))
            LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)
            return Response({"requires_2fa": True, "temp_token": temp_token, "token_type": "Bearer", "expires_in": 300})

        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))
        LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL, "requires_2fa": False})
        set_refresh_cookie(response, raw_refresh)
        return response



@login_phone_schema
class LoginPhoneView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginPhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserAuth.objects.get(phone=data["phone"])
        except UserAuth.DoesNotExist:
            return Response({"message": "OTP sent", "expires_in": settings.OTP_TTL})

        otp = TokenService.generate_otp()
        VerificationToken.objects.create(
            user=user, token_hash=TokenService.hash_token(otp),
            type="phone_otp", payload={"context": "login", "platform_id": str(data["platform_id"])},
            expires_at=timezone.now() + timedelta(seconds=settings.OTP_TTL),
        )

        NotificationClient.send(
            notification_type="phone_otp",
            recipient={"email": None, "phone": user.phone},
            template="auth_otp_sms",
            data={"otp_code": otp, "expires_in_minutes": settings.OTP_TTL // 60},
            priority="critical",
        )

        return Response({"message": "OTP sent", "expires_in": settings.OTP_TTL})



@magic_link_schema
class MagicLinkRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = MagicLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserAuth.objects.get(email=data["email"])
        except UserAuth.DoesNotExist:
            return Response({"message": "Magic link sent", "expires_in": settings.MAGIC_LINK_TTL})

        try:
            platform = Platform.objects.get(id=data["platform_id"], is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # VÃ©rifier redirect_url dans whitelist
        if data["redirect_url"] not in platform.allowed_redirect_urls:
            return Response({"detail": "redirect_url non autorisÃ©e."}, status=status.HTTP_400_BAD_REQUEST)

        raw_token = TokenService.generate_raw_token()
        VerificationToken.objects.create(
            user=user, token_hash=TokenService.hash_token(raw_token),
            type="magic_link",
            payload={"platform_id": str(platform.id), "redirect_url": data["redirect_url"]},
            expires_at=timezone.now() + timedelta(seconds=settings.MAGIC_LINK_TTL),
        )

        callback_url = f"{request.scheme}://{request.get_host()}/api/v1/auth/magic-link/callback?token={raw_token}"

        NotificationClient.send(
            notification_type="magic_link",
            recipient={"email": user.email, "phone": None},
            template="auth_magic_link",
            data={"magic_link_url": callback_url, "expires_in_minutes": settings.MAGIC_LINK_TTL // 60, "platform_name": platform.name},
            priority="high",
        )

        return Response({"message": "Magic link sent", "expires_in": settings.MAGIC_LINK_TTL})



@magic_link_callback_schema
class MagicLinkCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        raw_token = request.GET.get("token")
        if not raw_token:
            return Response({"detail": "Token manquant."}, status=status.HTTP_400_BAD_REQUEST)

        token_hash = TokenService.hash_token(raw_token)
        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="magic_link")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "Token expirÃ© ou dÃ©jÃ  utilisÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        user = vtoken.user
        available, reason = user.is_available_for_login
        if not available:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        payload = vtoken.payload or {}
        platform_id = payload.get("platform_id")
        redirect_url = payload.get("redirect_url", "/")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

        LoginHistory.objects.create(user=user, platform=platform, method="magic_link", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        response = django_redirect(redirect_url)
        set_access_cookie(response, access_token)
        set_refresh_cookie(response, raw_refresh)
        return response

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\views_sessions.py =====
`
"""
AGT Auth Service v1.0 â€” Views : Sessions, Tokens, 2FA, Password, Profile, Audit.
"""
import logging
from datetime import timedelta, datetime

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import Session, RefreshToken, VerificationToken, LoginHistory, UserAuth
from apps.authentication.pagination import StandardPagination
from apps.authentication.serializers import (
    ChangePasswordSerializer, ResetPasswordSerializer, ForgotPasswordSerializer,
    TwoFAConfirmSerializer, TwoFAVerifySerializer, TwoFADisableSerializer,
    SessionResponseSerializer, LoginHistoryResponseSerializer, UserAuthResponseSerializer,
)
from apps.authentication.services import JWTService, TokenService, TOTPService, SessionService, NotificationClient
from apps.authentication.utils import get_client_ip, set_refresh_cookie, clear_refresh_cookie, clear_access_cookie
from apps.authentication.swagger import (
    refresh_schema, logout_schema, session_list_schema, session_revoke_schema,
    verify_token_schema, token_exchange_schema, forgot_password_schema, reset_password_schema,
    change_password_schema, twofa_enable_schema, twofa_confirm_schema, twofa_verify_schema,
    twofa_disable_schema, me_schema, login_history_schema, user_stats_schema,
)

logger = logging.getLogger(__name__)



@refresh_schema
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_refresh = request.COOKIES.get("refresh_token")
        if not raw_refresh:
            return Response({"detail": "Refresh token manquant."}, status=status.HTTP_401_UNAUTHORIZED)

        token_hash = TokenService.hash_refresh_token(raw_refresh)
        try:
            rt = RefreshToken.objects.select_related("user", "session", "session__platform").get(token_hash=token_hash, is_revoked=False)
        except RefreshToken.DoesNotExist:
            return Response({"detail": "Refresh token invalide ou rÃ©voquÃ©."}, status=status.HTTP_401_UNAUTHORIZED)

        if rt.is_expired():
            return Response({"detail": "Refresh token expirÃ©."}, status=status.HTTP_401_UNAUTHORIZED)

        user = rt.user
        available, reason = user.is_available_for_login
        if not available:
            return Response({"valid": False, "reason": reason}, status=status.HTTP_403_FORBIDDEN)

        session = rt.session
        if not session.is_active or session.is_expired():
            return Response({"detail": "Session expirÃ©e."}, status=status.HTTP_401_UNAUTHORIZED)

        rt.revoke()
        new_raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(session.platform_id), str(session.id))

        response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
        set_refresh_cookie(response, new_raw_refresh)
        return response



@logout_schema
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = request.auth
        session_id = payload.get("session_id") if payload else None
        if session_id:
            try:
                session = Session.objects.get(id=session_id)
                SessionService.revoke_session(session)
            except Session.DoesNotExist:
                pass

        response = Response({"message": "Logged out successfully"})
        clear_refresh_cookie(response)
        return response



@session_list_schema
class SessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = request.auth
        current_session_id = payload.get("session_id") if payload else None
        sessions = Session.objects.filter(user=request.user, is_active=True).select_related("platform")
        paginator = StandardPagination()
        page = paginator.paginate_queryset(sessions, request)
        serializer = SessionResponseSerializer(page, many=True, context={"current_session_id": current_session_id})
        return paginator.get_paginated_response(serializer.data)



@session_revoke_schema
class SessionRevokeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id, user=request.user, is_active=True)
        except Session.DoesNotExist:
            return Response({"detail": "Session introuvable."}, status=status.HTTP_404_NOT_FOUND)
        SessionService.revoke_session(session)
        return Response({"message": "Session revoked"})



@verify_token_schema
class VerifyTokenView(APIView):
    """Endpoint interne â€” vÃ©rifie un JWT utilisateur (6 vÃ©rifications CDC)."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return Response({"valid": False, "reason": "missing_token"}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ", 1)[1]
        try:
            payload = JWTService.decode_token(token)
        except jwt.ExpiredSignatureError:
            return Response({"valid": False, "reason": "token_expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"valid": False, "reason": "invalid_signature"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserAuth.objects.get(id=payload["sub"])
        except UserAuth.DoesNotExist:
            return Response({"valid": False, "reason": "user_not_found"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_blocked:
            return Response({"valid": False, "reason": "user_blocked"}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_deactivated:
            return Response({"valid": False, "reason": "user_deactivated"}, status=status.HTTP_401_UNAUTHORIZED)

        session_id = payload.get("session_id")
        try:
            session = Session.objects.select_related("platform").get(id=session_id)
        except Session.DoesNotExist:
            return Response({"valid": False, "reason": "session_revoked"}, status=status.HTTP_401_UNAUTHORIZED)

        if not session.is_active or session.is_expired():
            return Response({"valid": False, "reason": "session_revoked"}, status=status.HTTP_401_UNAUTHORIZED)
        if not session.platform.is_active:
            return Response({"valid": False, "reason": "platform_inactive"}, status=status.HTTP_401_UNAUTHORIZED)

        expires_at = datetime.utcfromtimestamp(payload["exp"]).isoformat() + "Z"
        return Response({"valid": True, "user_id": str(user.id), "platform_id": payload.get("platform_id"), "expires_at": expires_at})



@token_exchange_schema
class TokenExchangeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_access = request.COOKIES.get("access_token")
        if not raw_access:
            return Response({"detail": "Cookie access_token absent."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            JWTService.decode_token(raw_access)
        except jwt.InvalidTokenError:
            return Response({"detail": "Token invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"access_token": raw_access, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
        clear_access_cookie(response)
        return response



@forgot_password_schema
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = UserAuth.objects.get(email=email)
            raw_token = TokenService.generate_raw_token()
            VerificationToken.objects.create(
                user=user, token_hash=TokenService.hash_token(raw_token),
                type="password_reset",
                expires_at=timezone.now() + timedelta(hours=1),
            )
            NotificationClient.send(
                notification_type="password_reset",
                recipient={"email": email, "phone": None},
                template="auth_reset_password",
                data={"reset_url": f"{request.scheme}://{request.get_host()}/api/v1/auth/reset-password?token={raw_token}", "expires_in_minutes": 60},
                priority="high",
            )
        except UserAuth.DoesNotExist:
            pass

        return Response({"message": "Reset link sent if account exists"})



@reset_password_schema
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        token_hash = TokenService.hash_token(data["token"])

        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="password_reset")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "Token expirÃ© ou dÃ©jÃ  utilisÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        user = vtoken.user
        user.set_password(data["new_password"])
        user.save(update_fields=["password_hash", "updated_at"])
        SessionService.revoke_all_sessions(user)

        return Response({"message": "Password reset successfully"})



@change_password_schema
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response({"detail": "Mot de passe actuel incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password_hash", "updated_at"])

        current_session_id = request.auth.get("session_id") if request.auth else None
        SessionService.revoke_all_sessions(user, except_session_id=current_session_id)

        return Response({"message": "Password changed successfully"})



@twofa_enable_schema
class TwoFAEnableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.two_fa_enabled:
            return Response({"detail": "2FA dÃ©jÃ  activÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        secret = TOTPService.generate_secret()
        user.two_fa_secret = TOTPService.encrypt_secret(secret)
        user.save(update_fields=["two_fa_secret", "updated_at"])

        return Response({
            "secret": secret,
            "qr_code_url": TOTPService.get_totp_uri(secret, user.email or str(user.id)),
            "message": "Scan QR code, then verify with POST /auth/2fa/confirm",
        })



@twofa_confirm_schema
class TwoFAConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwoFAConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.two_fa_secret:
            return Response({"detail": "2FA non initialisÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        secret = TOTPService.decrypt_secret(user.two_fa_secret)
        if not TOTPService.verify_code(secret, serializer.validated_data["code"]):
            return Response({"detail": "Code invalide."}, status=status.HTTP_400_BAD_REQUEST)

        user.two_fa_enabled = True
        user.save(update_fields=["two_fa_enabled", "updated_at"])

        return Response({"message": "2FA activated", "two_fa_enabled": True})



@twofa_verify_schema
class TwoFAVerifyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = TwoFAVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            payload = JWTService.decode_token(data["temp_token"])
        except jwt.InvalidTokenError:
            return Response({"detail": "Temp token invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        if payload.get("type") != "2fa_challenge":
            return Response({"detail": "Token type invalide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAuth.objects.get(id=payload["sub"])
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        secret = TOTPService.decrypt_secret(user.two_fa_secret)
        if not TOTPService.verify_code(secret, data["code"]):
            return Response({"detail": "Code 2FA invalide."}, status=status.HTTP_400_BAD_REQUEST)

        access_token = JWTService.generate_access_token_2fa(user, payload["platform_id"], payload["session_id"])
        response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
        return response



@twofa_disable_schema
class TwoFADisableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwoFADisableSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.two_fa_enabled:
            return Response({"detail": "2FA non activÃ©."}, status=status.HTTP_400_BAD_REQUEST)

        secret = TOTPService.decrypt_secret(user.two_fa_secret)
        if not TOTPService.verify_code(secret, serializer.validated_data["code"]):
            return Response({"detail": "Code invalide."}, status=status.HTTP_400_BAD_REQUEST)

        user.two_fa_enabled = False
        user.two_fa_secret = None
        user.save(update_fields=["two_fa_enabled", "two_fa_secret", "updated_at"])

        return Response({"message": "2FA disabled", "two_fa_enabled": False})



@me_schema
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserAuthResponseSerializer(request.user).data)



@login_history_schema
class LoginHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = LoginHistory.objects.filter(user=request.user).select_related("platform")
        platform_slug = request.GET.get("platform")
        if platform_slug:
            history = history.filter(platform__slug=platform_slug)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(history, request)
        return paginator.get_paginated_response(LoginHistoryResponseSerializer(page, many=True).data)



@user_stats_schema
class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = UserAuth.objects.get(id=user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        total_logins = LoginHistory.objects.filter(user=user, success=True).count()
        last_login = LoginHistory.objects.filter(user=user, success=True).order_by("-created_at").values_list("created_at", flat=True).first()
        active_sessions = Session.objects.filter(user=user, is_active=True).count()

        return Response({
            "user_id": str(user.id),
            "total_logins": total_logins,
            "last_login": last_login.isoformat() if last_login else None,
            "active_sessions": active_sessions,
        })

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\commands\cleanup_expired.py =====
`
"""
Commande Django : purge des donnÃ©es expirÃ©es.
Usage : python manage.py cleanup_expired
Cron quotidien recommandÃ©.
"""
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

from apps.authentication.models import Session, RefreshToken, VerificationToken


class Command(BaseCommand):
    help = "Purge les sessions expirÃ©es, refresh tokens rÃ©voquÃ©s et verification tokens expirÃ©s."

    def handle(self, *args, **options):
        now = timezone.now()

        sessions_deleted, _ = Session.objects.filter(expires_at__lt=now).delete()

        rt_deleted, _ = RefreshToken.objects.filter(
            models.Q(expires_at__lt=now) | models.Q(is_revoked=True)
        ).delete()

        vt_deleted, _ = VerificationToken.objects.filter(
            models.Q(expires_at__lt=now) | models.Q(used_at__isnull=False)
        ).delete()

        self.stdout.write(self.style.SUCCESS(
            f"Nettoyage : sessions={sessions_deleted}, refresh_tokens={rt_deleted}, verification_tokens={vt_deleted}"
        ))

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\commands\generate_keys.py =====
`
"""
Commande Django : gÃ©nÃ©ration des clÃ©s RSA RS256.
Usage : python manage.py generate_keys
"""
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "GÃ©nÃ¨re les clÃ©s RSA RS256 pour la signature JWT."

    def add_arguments(self, parser):
        parser.add_argument("--output-dir", type=str, default="keys", help="Dossier de sortie")
        parser.add_argument("--key-size", type=int, default=2048, help="Taille de la clÃ© (bits)")

    def handle(self, *args, **options):
        output_dir = Path(options["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)

        private_key = rsa.generate_private_key(public_exponent=65537, key_size=options["key_size"])

        private_path = output_dir / "private.pem"
        private_path.write_bytes(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
        private_path.chmod(0o600)

        public_path = output_dir / "public.pem"
        public_path.write_bytes(private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

        self.stdout.write(self.style.SUCCESS(f"ClÃ©s gÃ©nÃ©rÃ©es : {private_path}, {public_path}"))

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\management\commands\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\tests\test_all.py =====
`
"""
AGT Auth Service v1.0 â€” Tests unitaires et d'intÃ©gration.
"""
import uuid
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.authentication.models import (
    Platform, UserAuth, Session, RefreshToken, VerificationToken, LoginHistory,
)
from apps.authentication.services import JWTService, TokenService, TOTPService, SessionService


# â”€â”€â”€ Helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def make_platform(**kwargs):
    defaults = {
        "name": f"Platform-{uuid.uuid4().hex[:6]}",
        "slug": f"plat-{uuid.uuid4().hex[:6]}",
        "allowed_auth_methods": ["email", "phone", "google", "magic_link"],
        "allowed_redirect_urls": ["http://localhost:3000/callback"],
        "client_secret_hash": Platform.hash_client_secret("test-secret"),
        "is_active": True,
    }
    defaults.update(kwargs)
    return Platform.objects.create(**defaults)


def make_user(platform, **kwargs):
    defaults = {
        "email": f"user-{uuid.uuid4().hex[:6]}@agt.com",
        "registration_method": "email",
        "registration_platform": platform,
    }
    defaults.update(kwargs)
    user = UserAuth(**defaults)
    user.set_password(kwargs.get("password", "SecureP@ss123!"))
    user.save()
    return user


# â”€â”€â”€ Tests ModÃ¨les â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestUserAuthModel(TestCase):
    def setUp(self):
        self.platform = make_platform()

    def test_set_and_check_password(self):
        user = make_user(self.platform)
        self.assertTrue(user.check_password("SecureP@ss123!"))
        self.assertFalse(user.check_password("Wrong"))

    def test_password_not_plain_text(self):
        user = make_user(self.platform)
        self.assertNotEqual(user.password_hash, "SecureP@ss123!")
        self.assertTrue(user.password_hash.startswith("$2b$"))

    def test_is_available_blocked(self):
        user = make_user(self.platform)
        user.is_blocked = True
        user.save()
        available, reason = user.is_available_for_login
        self.assertFalse(available)
        self.assertEqual(reason, "user_blocked")

    def test_is_available_deactivated(self):
        user = make_user(self.platform)
        user.is_deactivated = True
        user.save()
        available, reason = user.is_available_for_login
        self.assertFalse(available)
        self.assertEqual(reason, "user_deactivated")

    def test_brute_force_lockout(self):
        user = make_user(self.platform)
        for _ in range(5):
            user.increment_failed_attempts()
        user.refresh_from_db()
        self.assertTrue(user.is_locked())


# â”€â”€â”€ Tests Services â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestJWTService(TestCase):
    def setUp(self):
        self.platform = make_platform()
        self.user = make_user(self.platform)

    def test_generate_and_decode_token(self):
        token = JWTService.generate_access_token(self.user, str(self.platform.id), str(uuid.uuid4()))
        payload = JWTService.decode_token(token)
        self.assertEqual(payload["sub"], str(self.user.id))
        self.assertEqual(payload["iss"], "agt-auth")

    def test_s2s_token(self):
        token = JWTService.generate_s2s_token(str(self.platform.id), self.platform.name)
        payload = JWTService.decode_token(token)
        self.assertEqual(payload["type"], "s2s")


class TestTokenService(TestCase):
    def test_hash_deterministic(self):
        token = "test-token-123"
        h1 = TokenService.hash_token(token)
        h2 = TokenService.hash_token(token)
        self.assertEqual(h1, h2)

    def test_otp_length(self):
        otp = TokenService.generate_otp(6)
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())


class TestSessionService(TestCase):
    def setUp(self):
        self.platform = make_platform()
        self.user = make_user(self.platform)

    def test_create_session(self):
        session = SessionService.create_session(self.user, self.platform, "127.0.0.1")
        self.assertTrue(session.is_active)
        self.assertFalse(session.is_expired())

    def test_refresh_token_fifo(self):
        session = SessionService.create_session(self.user, self.platform, "127.0.0.1")
        tokens = []
        for _ in range(6):
            tokens.append(SessionService.create_refresh_token(self.user, session))
        active = RefreshToken.objects.filter(user=self.user, is_revoked=False).count()
        self.assertLessEqual(active, 5)

    def test_revoke_all_sessions(self):
        s1 = SessionService.create_session(self.user, self.platform, "127.0.0.1")
        s2 = SessionService.create_session(self.user, self.platform, "127.0.0.2")
        SessionService.revoke_all_sessions(self.user)
        s1.refresh_from_db()
        s2.refresh_from_db()
        self.assertFalse(s1.is_active)
        self.assertFalse(s2.is_active)


# â”€â”€â”€ Tests Endpoints â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        response = client.get("/api/v1/auth/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["version"], "1.0.0")


class TestRegisterEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()

    @patch("apps.authentication.services.NotificationClient.send", return_value=True)
    @patch("apps.authentication.services.UsersServiceClient.provision_user", return_value=True)
    def test_register_email(self, mock_users, mock_notif):
        response = self.client.post(
            "/api/v1/auth/register",
            data={"email": "new@agt.com", "password": "SecureP@ss123!", "method": "email"},
            format="json",
            HTTP_X_PLATFORM_ID=str(self.platform.id),
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertTrue(UserAuth.objects.filter(email="new@agt.com").exists())

    def test_register_missing_platform(self):
        response = self.client.post(
            "/api/v1/auth/register",
            data={"email": "x@x.com", "password": "Pass1234!", "method": "email"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    @patch("apps.authentication.services.NotificationClient.send", return_value=True)
    @patch("apps.authentication.services.UsersServiceClient.provision_user", return_value=True)
    def test_register_duplicate_email(self, mock_users, mock_notif):
        make_user(self.platform, email="dup@agt.com")
        response = self.client.post(
            "/api/v1/auth/register",
            data={"email": "dup@agt.com", "password": "SecureP@ss123!", "method": "email"},
            format="json",
            HTTP_X_PLATFORM_ID=str(self.platform.id),
        )
        self.assertEqual(response.status_code, 409)


class TestLoginEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()
        self.user = make_user(self.platform, email="login@agt.com")

    def test_login_success(self):
        response = self.client.post("/api/v1/auth/login", data={
            "email": "login@agt.com", "password": "SecureP@ss123!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_login_wrong_password(self):
        response = self.client.post("/api/v1/auth/login", data={
            "email": "login@agt.com", "password": "WrongPass!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(response.status_code, 401)

    def test_login_blocked_user(self):
        self.user.is_blocked = True
        self.user.save()
        response = self.client.post("/api/v1/auth/login", data={
            "email": "login@agt.com", "password": "SecureP@ss123!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(response.status_code, 403)


class TestRefreshEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()
        self.user = make_user(self.platform, email="refresh@agt.com")

    def test_refresh_with_valid_cookie(self):
        login_resp = self.client.post("/api/v1/auth/login", data={
            "email": "refresh@agt.com", "password": "SecureP@ss123!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(login_resp.status_code, 200)

        refresh_cookie = login_resp.cookies.get("refresh_token")
        self.assertIsNotNone(refresh_cookie)

        self.client.cookies["refresh_token"] = refresh_cookie.value
        response = self.client.post("/api/v1/auth/refresh")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_refresh_without_cookie(self):
        response = self.client.post("/api/v1/auth/refresh")
        self.assertEqual(response.status_code, 401)


class TestAdminEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()
        self.user = make_user(self.platform, email="admin_target@agt.com")

    def _admin_headers(self):
        return {"HTTP_X_ADMIN_API_KEY": settings.ADMIN_API_KEY}

    def test_block_user(self):
        response = self.client.post(f"/api/v1/auth/admin/block/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_blocked)

    def test_unblock_user(self):
        self.user.is_blocked = True
        self.user.save()
        response = self.client.post(f"/api/v1/auth/admin/unblock/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_blocked)

    @patch("apps.authentication.services.UsersServiceClient.sync_status", return_value=True)
    def test_admin_deactivate(self, mock_sync):
        response = self.client.post(f"/api/v1/auth/admin/deactivate/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_deactivated)
        mock_sync.assert_called_once()

    def test_admin_purge(self):
        response = self.client.delete(f"/api/v1/auth/admin/purge/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserAuth.objects.filter(id=self.user.id).exists())

    def test_admin_requires_key(self):
        response = self.client.post(f"/api/v1/auth/admin/block/{self.user.id}")
        self.assertIn(response.status_code, [401, 403])

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\authentication\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\serializers.py =====
`
"""
AGT Auth Service v1.0 â€” Platforms : Serializers.
"""
import secrets
import bcrypt
from rest_framework import serializers
from apps.authentication.models import Platform


class PlatformCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField(max_length=50)
    allowed_auth_methods = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "phone", "google", "facebook", "magic_link"]),
        min_length=1,
    )
    allowed_redirect_urls = serializers.ListField(child=serializers.URLField(), required=False, default=list)

    def validate_slug(self, value):
        if Platform.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Ce slug est dÃ©jÃ  utilisÃ©.")
        return value

    def validate_name(self, value):
        if Platform.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ce nom est dÃ©jÃ  utilisÃ©.")
        return value


class PlatformUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=False)
    allowed_auth_methods = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "phone", "google", "facebook", "magic_link"]),
        required=False,
    )
    allowed_redirect_urls = serializers.ListField(child=serializers.URLField(), required=False)
    is_active = serializers.BooleanField(required=False)


class PlatformResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "name", "slug", "allowed_auth_methods", "allowed_redirect_urls", "is_active", "created_at", "updated_at"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\urls.py =====
`
from django.urls import path
from apps.platforms.views import PlatformListCreateView, PlatformDetailView

urlpatterns = [
    path("auth/platforms", PlatformListCreateView.as_view(), name="platforms-list-create"),
    path("auth/platforms/<uuid:platform_id>", PlatformDetailView.as_view(), name="platforms-detail"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\views.py =====
`
from apps.authentication.swagger import platform_list_create_schema, platform_detail_schema
"""
AGT Auth Service v1.0 â€” Platforms : Views CRUD admin.
"""
import secrets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import Platform
from apps.authentication.permissions import IsAdminAPIKey
from apps.platforms.serializers import PlatformCreateSerializer, PlatformUpdateSerializer, PlatformResponseSerializer



@platform_list_create_schema
class PlatformListCreateView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request):
        serializer = PlatformCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        raw_secret = secrets.token_urlsafe(48)

        platform = Platform.objects.create(
            name=data["name"],
            slug=data["slug"],
            allowed_auth_methods=data["allowed_auth_methods"],
            allowed_redirect_urls=data.get("allowed_redirect_urls", []),
            client_secret_hash=Platform.hash_client_secret(raw_secret),
        )

        response_data = PlatformResponseSerializer(platform).data
        response_data["client_secret"] = raw_secret  # AffichÃ© uniquement Ã  la crÃ©ation

        return Response(response_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        platforms = Platform.objects.all()
        return Response({"data": PlatformResponseSerializer(platforms, many=True).data})



@platform_detail_schema
class PlatformDetailView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def put(self, request, platform_id):
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlatformUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for field, value in serializer.validated_data.items():
            setattr(platform, field, value)
        platform.save()

        return Response(PlatformResponseSerializer(platform).data)

    def delete(self, request, platform_id):
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme introuvable."}, status=status.HTTP_404_NOT_FOUND)

        platform.is_active = False
        platform.save(update_fields=["is_active", "updated_at"])

        return Response({"message": "Platform deactivated", "is_active": False})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\apps\platforms\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\common\middleware.py =====
`
"""
AGT Auth Service v1.0 â€” Middleware : Rate limiting Redis + CSRF cookie protection.
"""
import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """Rate limiting par endpoint + global par IP via Redis incr/expire."""

    RATE_LIMITS = {
        "/api/v1/auth/login": {"window": 60, "max": 10},
        "/api/v1/auth/login/phone": {"window": 60, "max": 3},
        "/api/v1/auth/verify-otp": {"window": 60, "max": 5},
        "/api/v1/auth/forgot-password": {"window": 900, "max": 3},
        "/api/v1/auth/register": {"window": 3600, "max": 5},
        "/api/v1/auth/2fa/verify": {"window": 60, "max": 5},
    }

    GLOBAL_WINDOW = 60
    GLOBAL_MAX = 100

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self._get_ip(request)
        path = request.path.rstrip("/")

        # Endpoint-specific
        rule = self.RATE_LIMITS.get(path)
        if rule and request.method == "POST":
            key = f"rl:{path}:{ip}"
            if self._is_limited(key, rule["window"], rule["max"]):
                return JsonResponse(
                    {"success": False, "error": {"code": "RATE_LIMITED", "message": "Trop de requÃªtes."}},
                    status=429,
                )

        # Global
        if self._is_limited(f"rl:global:{ip}", self.GLOBAL_WINDOW, self.GLOBAL_MAX):
            return JsonResponse(
                {"success": False, "error": {"code": "RATE_LIMITED", "message": "Trop de requÃªtes."}},
                status=429,
            )

        return self.get_response(request)

    def _is_limited(self, key, window, max_requests):
        try:
            current = cache.get(key, 0)
            if current >= max_requests:
                return True
            # IncrÃ©mente atomiquement avec TTL
            if current == 0:
                cache.set(key, 1, timeout=window)
            else:
                cache.incr(key)
            return False
        except Exception:
            return False  # Fail-open

    @staticmethod
    def _get_ip(request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", "0.0.0.0")


class CSRFCookieProtectionMiddleware:
    """Protection CSRF sur endpoints cookie-based (CDC v1.3.2)."""

    PROTECTED_PATHS = {
        "/api/v1/auth/refresh",
        "/api/v1/auth/logout",
        "/api/v1/auth/token/exchange",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip("/")

        if request.method == "POST" and path in self.PROTECTED_PATHS:
            if not getattr(settings, "DEBUG", False):
                xrw = request.headers.get("X-Requested-With", "")
                origin = request.headers.get("Origin", "")
                allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", [])
                if isinstance(allowed, str):
                    allowed = [a.strip() for a in allowed.split(",")]

                if xrw != "XMLHttpRequest" and origin and origin not in allowed:
                    return JsonResponse(
                        {"success": False, "error": {"code": "CSRF_FAILED", "message": "RequÃªte non autorisÃ©e."}},
                        status=403,
                    )

        return self.get_response(request)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\settings.py =====
`
"""
AGT Auth Service v1.0 â€” Django Settings
"""
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# â”€â”€â”€ SÃ©curitÃ© â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

# â”€â”€â”€ Applications â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "apps.authentication",
    "apps.platforms",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.RateLimitMiddleware",
    "common.middleware.CSRFCookieProtectionMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# â”€â”€â”€ Base de donnÃ©es â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
import dj_database_url  # noqa: E402

DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
        ssl_require=False,
    )
}

# â”€â”€â”€ Cache (Redis) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
        },
    }
}

# â”€â”€â”€ JWT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def _read_key(path_env_var: str, default_path: str) -> str:
    path = config(path_env_var, default=default_path)
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


JWT_PRIVATE_KEY = _read_key("JWT_PRIVATE_KEY_PATH", str(BASE_DIR / "keys/private.pem"))
JWT_PUBLIC_KEY = _read_key("JWT_PUBLIC_KEY_PATH", str(BASE_DIR / "keys/public.pem"))
JWT_ACCESS_TTL = config("JWT_ACCESS_TTL", default=900, cast=int)
JWT_REFRESH_TTL = config("JWT_REFRESH_TTL", default=604800, cast=int)
JWT_ISSUER = config("JWT_ISSUER", default="agt-auth")
JWT_AUDIENCE = config("JWT_AUDIENCE", default="agt-ecosystem")

# â”€â”€â”€ SÃ©curitÃ© Auth â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BCRYPT_ROUNDS = config("BCRYPT_ROUNDS", default=12, cast=int)
ADMIN_API_KEY = config("ADMIN_API_KEY", default="")
MAX_REFRESH_TOKENS = config("MAX_REFRESH_TOKENS", default=5, cast=int)

# â”€â”€â”€ Tokens durÃ©es de vie â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
OTP_TTL = config("OTP_TTL", default=300, cast=int)
MAGIC_LINK_TTL = config("MAGIC_LINK_TTL", default=600, cast=int)

# â”€â”€â”€ Rate Limiting â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
RATE_LIMIT_LOGIN = config("RATE_LIMIT_LOGIN", default=10, cast=int)
BRUTE_FORCE_MAX = config("BRUTE_FORCE_MAX", default=5, cast=int)
BRUTE_FORCE_LOCKOUT = config("BRUTE_FORCE_LOCKOUT", default=900, cast=int)

# â”€â”€â”€ Services Inter-microservices â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", default="")
USERS_SERVICE_URL = config("USERS_SERVICE_URL", default="")

# â”€â”€â”€ OAuth â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET", default="")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI", default="")

FACEBOOK_APP_ID = config("FACEBOOK_APP_ID", default="")
FACEBOOK_APP_SECRET = config("FACEBOOK_APP_SECRET", default="")
FACEBOOK_REDIRECT_URI = config("FACEBOOK_REDIRECT_URI", default="")

# â”€â”€â”€ Cookies â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
COOKIE_SECURE = config("COOKIE_SECURE", default=False, cast=bool)
COOKIE_SAMESITE = config("COOKIE_SAMESITE", default="Lax")

# â”€â”€â”€ DRF â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.authentication.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.authentication.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.authentication.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

# â”€â”€â”€ Swagger / OpenAPI (drf-spectacular) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Auth Service API",
    "DESCRIPTION": "Service d'authentification centralise de l'ecosysteme AG Technologies.\n\nJWT RS256, OAuth Google/Facebook, 2FA TOTP, sessions, S2S tokens.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {"name": "AGT Engineering", "email": "engineering@agt.com"},
    "LICENSE": {"name": "Proprietary"},
    "TAGS": [
        {"name": "Health", "description": "Etat du service"},
        {"name": "Register", "description": "Inscription et verification"},
        {"name": "Login", "description": "Connexion (email, phone, magic link)"},
        {"name": "OAuth", "description": "Authentification sociale (Google, Facebook)"},
        {"name": "Password", "description": "Oubli, reset, changement de mot de passe"},
        {"name": "2FA", "description": "Authentification a double facteur (TOTP)"},
        {"name": "Sessions", "description": "Gestion sessions et tokens"},
        {"name": "Profile", "description": "Profil identite et audit"},
        {"name": "Admin", "description": "Administration (block, deactivate, purge)"},
        {"name": "Platforms", "description": "CRUD plateformes (admin)"},
        {"name": "S2S", "description": "Tokens inter-services (machine-to-machine)"},
    ],
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
    },
}

# â”€â”€â”€ CORS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

# â”€â”€â”€ Logging â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "apps": {"level": "DEBUG" if DEBUG else "INFO"},
    },
}

# â”€â”€â”€ Static files â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\settings_test.py =====
`
"""
Settings de test â€” base SQLite en mÃ©moire, cache local, clÃ©s RSA de test.
"""
from config.settings import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

_test_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
JWT_PRIVATE_KEY = _test_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption(),
).decode()
JWT_PUBLIC_KEY = _test_private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode()

BCRYPT_ROUNDS = 4
ADMIN_API_KEY = "test-admin-key-for-tests-only"
NOTIFICATION_SERVICE_URL = ""
USERS_SERVICE_URL = ""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {"null": {"class": "logging.NullHandler"}},
    "root": {"handlers": ["null"]},
}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("api/v1/", include("apps.authentication.urls")),
    path("api/v1/", include("apps.platforms.urls")),

    # Swagger / OpenAPI 3.0
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-auth\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\.env.example =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://chatbot_user:chatbot_password@db:5432/agt_chatbot_db
REDIS_URL=redis://redis:6379/8
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\CDC_v1.0.md =====
`
# AGT Chatbot Service - CDC v1.0

> Chatbot IA multi-provider. Pipeline 4 couches. Knowledge base. Flows conversationnels.

## Pipeline
1. Keywords/Intent matching (couche 1)
2. Conversation flows (couche 2)
3. AI generative - OpenAI/Anthropic (couche 3)
4. Fallback + transfert humain (couche 4)

## Tables (15)
bots, bot_configs, bot_channels, intents, intent_keywords, conversation_flows, flow_nodes,
knowledge_categories, knowledge_base_entries, ai_provider_configs, conversation_logs,
bot_stats, transfer_logs

## Multi-provider IA
OpenAI, Anthropic, configurable par bot. Strategy pattern + circuit breaker.

## Port : 7010

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_chatbot_db
    environment:
      POSTGRES_DB: agt_chatbot_db
      POSTGRES_USER: chatbot_user
      POSTGRES_PASSWORD: chatbot_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5440:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U chatbot_user -d agt_chatbot_db"]
      interval: 10s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    container_name: agt_chatbot_redis
    volumes:
      - redis_data:/data
    ports:
      - "6387:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  chatbot:
    build:
      context: .
      target: production
    container_name: agt_chatbot_service
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://chatbot_user:chatbot_password@db:5432/agt_chatbot_db
      REDIS_URL: redis://redis:6379/8
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7010:7010"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7010/api/v1/chatbot/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  chatbot-dev:
    build:
      context: .
      target: builder
    container_name: agt_chatbot_dev
    command: sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:7010"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://chatbot_user:chatbot_password@db:5432/agt_chatbot_db
      REDIS_URL: redis://redis:6379/8
      DEBUG: "True"
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7010:7010"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles:
      - dev
volumes:
  postgres_data:
  redis_data:

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 7010
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7010", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\manage.py =====
`
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == "__main__": main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\README.md =====
`
# AGT Chatbot Service - v1.0

Chatbot IA multi-provider avec pipeline 4 couches.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Documentation API
| URL | Description |
|-----|-------------|
| http://localhost:7010/api/v1/docs/ | Swagger UI |
| http://localhost:7010/api/v1/redoc/ | ReDoc |

## Tests
```bash
docker compose exec chatbot python -m pytest -v
```

## Endpoints
- CRUD /chatbot/bots
- POST/GET /chatbot/bots/{id}/intents (+ keywords)
- POST/GET /chatbot/bots/{id}/flows (+ nodes)
- POST/GET /chatbot/bots/{id}/knowledge/categories
- POST/GET /chatbot/bots/{id}/knowledge/entries
- POST/GET /chatbot/bots/{id}/ai-providers
- **POST /chatbot/converse** (endpoint principal - pipeline 4 couches)
- GET /chatbot/bots/{id}/stats
- POST /chatbot/transfers/{id}/callback

Port : **7010**

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\requirements.txt =====
`
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.4
PyJWT==2.8.0
cryptography==42.0.5
drf-spectacular==0.27.2
python-decouple==3.8
httpx==0.27.0
gunicorn==22.0.0
pytest==8.2.0
pytest-django==4.8.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\ai_providers\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\bots\models.py =====
`
"""AGT Chatbot Service v1.0 - Modeles complets."""
import uuid
from django.db import models


class Bot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    system_prompt = models.TextField(null=True, blank=True)
    fallback_message = models.TextField(default="Je n'ai pas compris. Pouvez-vous reformuler ?")
    human_transfer_after = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bots"
        ordering = ["-created_at"]


class BotConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="configs")
    config_key = models.CharField(max_length=100)
    config_value = models.TextField()

    class Meta:
        db_table = "bot_configs"
        unique_together = [("bot", "config_key")]


class BotChannel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="channels")
    channel = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "bot_channels"
        unique_together = [("bot", "channel")]


class Intent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="intents")
    name = models.CharField(max_length=100)
    response = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "intents"
        unique_together = [("bot", "name")]


class IntentKeyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name="keywords")
    keyword = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)

    class Meta:
        db_table = "intent_keywords"


class ConversationFlow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="flows")
    name = models.CharField(max_length=100)
    trigger_intent = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation_flows"


class FlowNode(models.Model):
    NODE_TYPES = [("message", "Message"), ("question", "Question"), ("condition", "Condition"), ("action", "Action")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(ConversationFlow, on_delete=models.CASCADE, related_name="nodes")
    type = models.CharField(max_length=20, choices=NODE_TYPES)
    content = models.JSONField()
    next_node = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    branches = models.JSONField(null=True, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = "flow_nodes"
        ordering = ["position"]


class KnowledgeCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="kb_categories")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "knowledge_categories"
        unique_together = [("bot", "name")]


class KnowledgeBaseEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="kb_entries")
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    embedding = models.JSONField(null=True, blank=True)  # pgvector en prod
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "knowledge_base_entries"


class AiProviderConfig(models.Model):
    PURPOSE_CHOICES = [("conversation", "Conversation"), ("rag", "RAG"), ("translation", "Translation"), ("fallback", "Fallback")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="ai_providers")
    provider = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    api_key_encrypted = models.TextField(null=True, blank=True)
    base_url = models.CharField(max_length=500, null=True, blank=True)
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    max_tokens = models.IntegerField(default=1000)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    circuit_breaker_threshold = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_provider_configs"
        unique_together = [("bot", "provider", "purpose")]


class ConversationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="conversation_logs")
    conversation_id = models.UUIDField(db_index=True)
    sender_id = models.UUIDField()
    channel = models.CharField(max_length=30)
    user_message = models.TextField()
    bot_response = models.TextField()
    layer_used = models.CharField(max_length=30)
    intent_detected = models.CharField(max_length=100, null=True, blank=True)
    confidence = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    provider_used = models.CharField(max_length=30, null=True, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    processing_time_ms = models.IntegerField()
    is_resolved = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation_logs"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["bot", "created_at"]), models.Index(fields=["bot", "is_resolved"])]


class BotStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="stats")
    date = models.DateField()
    total_messages = models.IntegerField(default=0)
    resolved_count = models.IntegerField(default=0)
    fallback_count = models.IntegerField(default=0)
    human_transfer_count = models.IntegerField(default=0)
    layer1_count = models.IntegerField(default=0)
    layer2_count = models.IntegerField(default=0)
    layer3_count = models.IntegerField(default=0)
    top_intents = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "bot_stats"
        unique_together = [("bot", "date")]


class TransferLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="transfer_logs")
    conversation_id = models.UUIDField()
    chat_transfer_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField()
    reason = models.CharField(max_length=50, null=True, blank=True)
    bot_history = models.JSONField(null=True, blank=True)
    context = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default="sent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transfer_logs"
        ordering = ["-created_at"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\bots\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\orchestrator.py =====
`
"""AGT Chatbot Service v1.0 - Conversation Orchestrator. Pipeline 4 couches."""
import logging, time, uuid, httpx
from django.core.cache import cache
from apps.bots.models import Bot, Intent, IntentKeyword, ConversationFlow, AiProviderConfig, ConversationLog

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, bot, sender_id, message, channel, conversation_id=None):
        self.bot = bot
        self.sender_id = sender_id
        self.message = message
        self.channel = channel
        self.conv_id = conversation_id or str(uuid.uuid4())
        self.context = self._load_context()
        self.start_time = time.time()

    def process(self):
        # Couche 1 : Keywords / Intent matching
        result = self._layer1_keywords()
        if result:
            return self._finalize(result, "layer_1_keywords")

        # Couche 2 : Conversation flows
        result = self._layer2_flow()
        if result:
            return self._finalize(result, "layer_2_flow")

        # Couche 3 : AI generative
        result = self._layer3_ai()
        if result:
            return self._finalize(result, "layer_3_ai")

        # Couche 4 : Fallback
        return self._layer4_fallback()

    def _layer1_keywords(self):
        intents = Intent.objects.filter(bot=self.bot, is_active=True).prefetch_related("keywords")
        msg_lower = self.message.lower()
        best_intent = None
        best_score = 0

        for intent in intents:
            score = 0
            for kw in intent.keywords.all():
                if kw.keyword.lower() in msg_lower:
                    score += float(kw.weight)
            if score > best_score:
                best_score = score
                best_intent = intent

        if best_intent and best_score >= 1.0:
            return {"response": best_intent.response, "intent": best_intent.name, "confidence": min(best_score, 1.0)}
        return None

    def _layer2_flow(self):
        # Verifier si un flow est actif en contexte
        active_flow_id = self.context.get("active_flow_id")
        if active_flow_id:
            # Continuer le flow existant (simplifie pour MVP)
            pass
        return None

    def _layer3_ai(self):
        providers = AiProviderConfig.objects.filter(
            bot=self.bot, purpose="conversation", is_active=True
        ).order_by("priority")

        for provider_cfg in providers:
            try:
                response = self._call_ai_provider(provider_cfg)
                if response:
                    return {"response": response, "provider": provider_cfg.provider, "model": provider_cfg.model}
            except Exception as e:
                logger.warning(f"AI provider {provider_cfg.provider} failed: {e}")
                continue
        return None

    def _call_ai_provider(self, cfg):
        messages = [{"role": "system", "content": self.bot.system_prompt or "Tu es un assistant utile."}]
        history = self.context.get("history", [])[-10:]
        messages.extend(history)
        messages.append({"role": "user", "content": self.message})

        if cfg.provider == "openai":
            return self._call_openai(cfg, messages)
        elif cfg.provider == "anthropic":
            return self._call_anthropic(cfg, messages)
        return None

    def _call_openai(self, cfg, messages):
        url = cfg.base_url or "https://api.openai.com/v1/chat/completions"
        try:
            resp = httpx.post(url, headers={"Authorization": f"Bearer {cfg.api_key_encrypted}",
                                             "Content-Type": "application/json"},
                               json={"model": cfg.model, "messages": messages,
                                     "temperature": float(cfg.temperature), "max_tokens": cfg.max_tokens},
                               timeout=15.0)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
        return None

    def _call_anthropic(self, cfg, messages):
        url = cfg.base_url or "https://api.anthropic.com/v1/messages"
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        user_msgs = [m for m in messages if m["role"] != "system"]
        try:
            resp = httpx.post(url, headers={"x-api-key": cfg.api_key_encrypted,
                                             "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
                               json={"model": cfg.model, "system": system, "messages": user_msgs,
                                     "max_tokens": cfg.max_tokens, "temperature": float(cfg.temperature)},
                               timeout=15.0)
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
        except Exception as e:
            logger.error(f"Anthropic call failed: {e}")
        return None

    def _layer4_fallback(self):
        fallbacks = self.context.get("consecutive_fallbacks", 0) + 1
        self.context["consecutive_fallbacks"] = fallbacks
        self._save_context()

        response = self.bot.fallback_message

        # Transfert humain si seuil atteint
        if fallbacks >= self.bot.human_transfer_after:
            response += "\n\nJe vous transfere vers un agent humain."
            # TODO: S2S call to Chat Service

        result = {"response": response, "is_fallback": True, "consecutive_fallbacks": fallbacks}
        self._log("layer_4_fallback", result)
        elapsed = int((time.time() - self.start_time) * 1000)
        return {"response": response, "conversation_id": self.conv_id, "layer": "layer_4_fallback",
                "is_resolved": False, "processing_time_ms": elapsed}

    def _finalize(self, result, layer):
        self.context["consecutive_fallbacks"] = 0
        self.context.setdefault("history", []).append({"role": "user", "content": self.message})
        self.context["history"].append({"role": "assistant", "content": result["response"]})
        self._save_context()
        self._log(layer, result)

        elapsed = int((time.time() - self.start_time) * 1000)
        return {"response": result["response"], "conversation_id": self.conv_id, "layer": layer,
                "intent": result.get("intent"), "confidence": result.get("confidence"),
                "provider": result.get("provider"), "is_resolved": True, "processing_time_ms": elapsed}

    def _load_context(self):
        key = f"conv:{self.bot.id}:{self.sender_id}"
        return cache.get(key) or {"history": [], "consecutive_fallbacks": 0}

    def _save_context(self):
        key = f"conv:{self.bot.id}:{self.sender_id}"
        cache.set(key, self.context, timeout=1800)

    def _log(self, layer, result):
        try:
            ConversationLog.objects.create(
                bot=self.bot, conversation_id=self.conv_id, sender_id=self.sender_id,
                channel=self.channel, user_message=self.message, bot_response=result["response"],
                layer_used=layer, intent_detected=result.get("intent"),
                confidence=result.get("confidence"), provider_used=result.get("provider"),
                processing_time_ms=int((time.time() - self.start_time) * 1000),
                is_resolved=layer != "layer_4_fallback",
            )
        except Exception as e:
            logger.error(f"Log failed: {e}")

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\urls.py =====
`
from django.urls import path
from apps.conversations.views import (
    HealthCheckView, BotListCreateView, BotDetailView,
    IntentListCreateView, FlowListCreateView,
    KBCategoryView, KBEntryView, AiProviderView,
    ConverseView, BotStatsView, TransferCallbackView,
)
urlpatterns = [
    path("chatbot/health", HealthCheckView.as_view()),
    path("chatbot/bots", BotListCreateView.as_view()),
    path("chatbot/bots/<uuid:bot_id>", BotDetailView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/intents", IntentListCreateView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/flows", FlowListCreateView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/knowledge/categories", KBCategoryView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/knowledge/entries", KBEntryView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/ai-providers", AiProviderView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/stats", BotStatsView.as_view()),
    path("chatbot/converse", ConverseView.as_view()),
    path("chatbot/transfers/<uuid:transfer_id>/callback", TransferCallbackView.as_view()),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\views.py =====
`
"""AGT Chatbot Service v1.0 - Views."""
import uuid, logging
from django.db.models import Count, Sum, Avg
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.bots.models import (
    Bot, BotConfig, BotChannel, Intent, IntentKeyword, ConversationFlow, FlowNode,
    KnowledgeCategory, KnowledgeBaseEntry, AiProviderConfig, ConversationLog, BotStats, TransferLog,
)
from apps.conversations.orchestrator import Orchestrator

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
            from django.db import connection; connection.ensure_connection()
        except Exception: db_ok = False
        try:
            from django.core.cache import cache; cache.set("h", "ok", 5); redis_ok = cache.get("h") == "ok"
        except Exception: redis_ok = False
        ok = db_ok and redis_ok
        return Response({"status": "healthy" if ok else "degraded", "database": "ok" if db_ok else "error",
                         "redis": "ok" if redis_ok else "error", "version": "1.0.0"},
                        status=status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE)


# --- Bots CRUD ---

class BotListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Bots"], summary="Creer un bot")
    def post(self, request):
        d = request.data
        bot = Bot.objects.create(platform_id=d.get("platform_id"), name=d["name"],
                                  description=d.get("description"), system_prompt=d.get("system_prompt"),
                                  fallback_message=d.get("fallback_message", "Je n'ai pas compris."),
                                  human_transfer_after=d.get("human_transfer_after", 3),
                                  created_by=getattr(request.user, "auth_user_id", None))
        for ch in d.get("channels", []):
            BotChannel.objects.create(bot=bot, channel=ch)
        return Response({"id": str(bot.id), "name": bot.name, "message": "Bot created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Bots"], summary="Lister les bots")
    def get(self, request):
        qs = Bot.objects.filter(is_active=True)
        pid = request.GET.get("platform_id")
        if pid: qs = qs.filter(platform_id=pid)
        data = [{"id": str(b.id), "name": b.name, "platform_id": str(b.platform_id), "is_active": b.is_active} for b in qs]
        return Response({"data": data})


class BotDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Bots"], summary="Detail bot")
    def get(self, request, bot_id):
        try: bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable."}, status=status.HTTP_404_NOT_FOUND)
        channels = [{"channel": c.channel, "is_active": c.is_active} for c in bot.channels.all()]
        return Response({"id": str(bot.id), "name": bot.name, "description": bot.description,
                         "system_prompt": bot.system_prompt, "fallback_message": bot.fallback_message,
                         "human_transfer_after": bot.human_transfer_after, "channels": channels})

    @extend_schema(tags=["Bots"], summary="Modifier bot")
    def put(self, request, bot_id):
        try: bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable."}, status=status.HTTP_404_NOT_FOUND)
        d = request.data
        for f in ["name", "description", "system_prompt", "fallback_message", "human_transfer_after", "is_active"]:
            if f in d: setattr(bot, f, d[f])
        bot.save()
        return Response({"message": "Bot updated"})

    @extend_schema(tags=["Bots"], summary="Supprimer bot")
    def delete(self, request, bot_id):
        try: bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable."}, status=status.HTTP_404_NOT_FOUND)
        bot.is_active = False
        bot.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "Bot deactivated"})


# --- Intents ---

class IntentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Intents"], summary="CRUD intentions")
    def post(self, request, bot_id):
        d = request.data
        intent = Intent.objects.create(bot_id=bot_id, name=d["name"], response=d.get("response"))
        for kw in d.get("keywords", []):
            IntentKeyword.objects.create(intent=intent, keyword=kw.get("keyword", kw) if isinstance(kw, dict) else kw,
                                          weight=kw.get("weight", 1.0) if isinstance(kw, dict) else 1.0)
        return Response({"id": str(intent.id), "name": intent.name}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        intents = Intent.objects.filter(bot_id=bot_id, is_active=True)
        data = [{"id": str(i.id), "name": i.name, "keywords": list(i.keywords.values_list("keyword", flat=True))} for i in intents]
        return Response({"data": data})


# --- Flows ---

class FlowListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Flows"], summary="CRUD conversation flows")
    def post(self, request, bot_id):
        d = request.data
        flow = ConversationFlow.objects.create(bot_id=bot_id, name=d["name"], trigger_intent=d.get("trigger_intent"))
        for n in d.get("nodes", []):
            FlowNode.objects.create(flow=flow, type=n["type"], content=n.get("content", {}),
                                     branches=n.get("branches"), position=n.get("position", 0))
        return Response({"id": str(flow.id), "name": flow.name}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        flows = ConversationFlow.objects.filter(bot_id=bot_id, is_active=True)
        data = [{"id": str(f.id), "name": f.name, "trigger_intent": f.trigger_intent, "nodes_count": f.nodes.count()} for f in flows]
        return Response({"data": data})


# --- Knowledge Base ---

class KBCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Knowledge"], summary="Categories knowledge base")
    def post(self, request, bot_id):
        cat = KnowledgeCategory.objects.create(bot_id=bot_id, name=request.data["name"])
        return Response({"id": str(cat.id), "name": cat.name}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        cats = KnowledgeCategory.objects.filter(bot_id=bot_id)
        return Response({"data": [{"id": str(c.id), "name": c.name} for c in cats]})


class KBEntryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Knowledge"], summary="CRUD entries knowledge base")
    def post(self, request, bot_id):
        d = request.data
        entry = KnowledgeBaseEntry.objects.create(bot_id=bot_id, category_id=d.get("category_id"),
                                                    question=d["question"], answer=d["answer"])
        return Response({"id": str(entry.id), "message": "Entry created"}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        qs = KnowledgeBaseEntry.objects.filter(bot_id=bot_id, is_active=True)
        cat_id = request.GET.get("category_id")
        if cat_id: qs = qs.filter(category_id=cat_id)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(e.id), "question": e.question, "answer": e.answer[:200]} for e in page]
        return paginator.get_paginated_response(data)


# --- AI Providers ---

class AiProviderView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AI Providers"], summary="Config providers IA par bot")
    def post(self, request, bot_id):
        d = request.data
        cfg = AiProviderConfig.objects.create(
            bot_id=bot_id, provider=d["provider"], model=d["model"],
            api_key_encrypted=d.get("api_key"), base_url=d.get("base_url"),
            temperature=d.get("temperature", 0.7), max_tokens=d.get("max_tokens", 1000),
            purpose=d.get("purpose", "conversation"), priority=d.get("priority", 0))
        return Response({"id": str(cfg.id), "provider": cfg.provider, "model": cfg.model}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        cfgs = AiProviderConfig.objects.filter(bot_id=bot_id, is_active=True)
        data = [{"id": str(c.id), "provider": c.provider, "model": c.model, "purpose": c.purpose, "priority": c.priority} for c in cfgs]
        return Response({"data": data})


# --- Converse (endpoint principal) ---

class ConverseView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Converse"], summary="Envoyer un message au bot (pipeline 4 couches)")
    def post(self, request):
        d = request.data
        bot_id = d.get("bot_id")
        try: bot = Bot.objects.get(id=bot_id, is_active=True)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable ou inactif."}, status=status.HTTP_404_NOT_FOUND)
        message = d.get("message", "")
        if not message: return Response({"detail": "message requis."}, status=status.HTTP_400_BAD_REQUEST)
        sender_id = d.get("sender_id") or getattr(request.user, "auth_user_id", str(uuid.uuid4()))
        channel = d.get("channel", "web")
        conv_id = d.get("conversation_id")
        orchestrator = Orchestrator(bot, sender_id, message, channel, conv_id)
        result = orchestrator.process()
        return Response(result)


# --- Stats ---

class BotStatsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Stats"], summary="Statistiques bot")
    def get(self, request, bot_id):
        total = ConversationLog.objects.filter(bot_id=bot_id).count()
        resolved = ConversationLog.objects.filter(bot_id=bot_id, is_resolved=True).count()
        avg_ms = ConversationLog.objects.filter(bot_id=bot_id).aggregate(a=Avg("processing_time_ms"))["a"] or 0
        by_layer = dict(ConversationLog.objects.filter(bot_id=bot_id).values_list("layer_used").annotate(c=Count("id")))
        return Response({"total_messages": total, "resolved": resolved,
                         "resolution_rate": round(resolved / total * 100, 1) if total else 0,
                         "avg_processing_ms": round(avg_ms, 1), "by_layer": by_layer})


# --- Transfer callback ---

class TransferCallbackView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Transfers"], summary="Callback transfert humain (depuis Chat Service)")
    def post(self, request, transfer_id):
        try:
            tl = TransferLog.objects.get(id=transfer_id)
        except TransferLog.DoesNotExist:
            return Response({"detail": "Transfer introuvable."}, status=status.HTTP_404_NOT_FOUND)
        tl.status = request.data.get("status", "closed")
        tl.save(update_fields=["status", "updated_at"])
        return Response({"message": "Transfer updated", "status": tl.status})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\tests\test_all.py =====
`
"""AGT Chatbot Service v1.0 - Tests."""
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from apps.bots.models import Bot, Intent, IntentKeyword, ConversationLog, KnowledgeBaseEntry
from apps.conversations.orchestrator import Orchestrator

def make_bot(**kw):
    defaults = {"platform_id": uuid.uuid4(), "name": "Test Bot", "system_prompt": "Tu es un assistant.",
                "fallback_message": "Je ne comprends pas.", "human_transfer_after": 3}
    defaults.update(kw)
    return Bot.objects.create(**defaults)

def add_intent(bot, name, response, keywords):
    intent = Intent.objects.create(bot=bot, name=name, response=response)
    for kw in keywords:
        IntentKeyword.objects.create(intent=intent, keyword=kw, weight=1.0)
    return intent

class TestBotModel(TestCase):
    def test_create_bot(self):
        bot = make_bot()
        self.assertTrue(bot.is_active)
        self.assertEqual(bot.human_transfer_after, 3)

class TestLayer1Keywords(TestCase):
    def test_intent_matching(self):
        bot = make_bot()
        add_intent(bot, "greeting", "Bonjour ! Comment puis-je aider ?", ["bonjour", "salut", "hello"])
        orch = Orchestrator(bot, uuid.uuid4(), "Bonjour tout le monde", "web")
        result = orch.process()
        self.assertTrue(result["is_resolved"])
        self.assertEqual(result["layer"], "layer_1_keywords")
        self.assertIn("Bonjour", result["response"])

    def test_no_match_fallback(self):
        bot = make_bot()
        orch = Orchestrator(bot, uuid.uuid4(), "xyz random text", "web")
        result = orch.process()
        self.assertFalse(result["is_resolved"])
        self.assertEqual(result["layer"], "layer_4_fallback")

class TestFallbackCounter(TestCase):
    def test_consecutive_fallbacks(self):
        bot = make_bot(human_transfer_after=2)
        sid = uuid.uuid4()
        r1 = Orchestrator(bot, sid, "incomprehensible", "web").process()
        self.assertEqual(r1["layer"], "layer_4_fallback")
        r2 = Orchestrator(bot, sid, "still incomprehensible", "web").process()
        self.assertIn("agent humain", r2["response"])

class TestConversationLog(TestCase):
    def test_log_created(self):
        bot = make_bot()
        add_intent(bot, "help", "Comment puis-je aider ?", ["aide", "help"])
        Orchestrator(bot, uuid.uuid4(), "aide moi", "web").process()
        self.assertEqual(ConversationLog.objects.count(), 1)
        log = ConversationLog.objects.first()
        self.assertTrue(log.is_resolved)

class TestHealthEndpoint(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/chatbot/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")

class TestBotEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    def test_create_bot(self):
        resp = self.client.post("/api/v1/chatbot/bots", data={
            "platform_id": str(uuid.uuid4()), "name": "Sales Bot",
            "system_prompt": "Tu vends des produits.", "channels": ["web", "whatsapp"],
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_converse_bot_not_found(self):
        resp = self.client.post("/api/v1/chatbot/converse", data={
            "bot_id": str(uuid.uuid4()), "message": "hello",
        }, format="json")
        self.assertEqual(resp.status_code, 404)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\conversations\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\apps\knowledge\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\common\authentication.py =====
`
import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.platform_id = p.get("platform_id")
        self.is_authenticated = True
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "): return None
        token = h.split(" ", 1)[1]
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached: return JWTPayload(cached), cached
        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk: raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try: payload = jwt.decode(token, pk, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError: raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError: raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload
    def authenticate_header(self, request): return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\settings.py =====
`
from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.staticfiles", "rest_framework", "drf_spectacular", "corsheaders", "apps.bots", "apps.knowledge", "apps.conversations", "apps.ai_providers"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]
import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/8")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL, "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
def _read_key(path):
    try:
        with open(path, "r") as f: return f.read()
    except FileNotFoundError: return ""
AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ["common.authentication.JWTAuthentication"], "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"], "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"], "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", "UNAUTHENTICATED_USER": None}
SPECTACULAR_SETTINGS = {"TITLE": "AGT Chatbot Service API", "VERSION": "1.0.0", "DESCRIPTION": "Chatbot IA multi-provider, pipeline 4 couches, knowledge base, flows.", "TAGS": [{"name": "Health"}, {"name": "Bots"}, {"name": "Intents"}, {"name": "Flows"}, {"name": "Knowledge"}, {"name": "AI Providers"}, {"name": "Converse"}, {"name": "Stats"}, {"name": "Transfers"}]}
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {"version": 1, "disable_existing_loggers": False, "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\settings_test.py =====
`
from config.settings import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
LOGGING = {"version": 1, "disable_existing_loggers": True, "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path("api/v1/", include("apps.conversations.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-chatbot\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\.env =====
`
# ============================================================
# AGT Notification Service v1.0 - Variables d'environnement
# ============================================================

# --- Django ---
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# --- Base de donnees ---
DATABASE_URL=postgresql://notif_user:notif_password@db:5432/agt_notification_db

# --- Redis ---
REDIS_URL=redis://redis:6379/2

# --- RabbitMQ (Celery broker) ---
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/3

# --- Auth (validation JWT) ---
AUTH_SERVICE_URL=http://auth-service:7000/api/v1
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem

# --- Users (resolution coordonnees) ---
USERS_SERVICE_URL=http://users-service:7001/api/v1

# --- Cache TTL ---
USER_CACHE_TTL=300
IDEMPOTENCY_TTL=86400

# --- Providers Email ---
SENDGRID_API_KEY=
MAILGUN_API_KEY=
MAILGUN_DOMAIN=
DEFAULT_FROM_EMAIL=noreply@agtechnologies.com

# --- Providers SMS ---
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=

# --- Push ---
FCM_SERVER_KEY=

# --- CORS ---
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\.env.example =====
`
# ============================================================
# AGT Notification Service v1.0 - Variables d'environnement
# ============================================================

# --- Django ---
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# --- Base de donnees ---
DATABASE_URL=postgresql://notif_user:notif_password@db:5432/agt_notification_db

# --- Redis ---
REDIS_URL=redis://redis:6379/2

# --- RabbitMQ (Celery broker) ---
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/3

# --- Auth (validation JWT) ---
AUTH_SERVICE_URL=http://auth-service:7000/api/v1
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem

# --- Users (resolution coordonnees) ---
USERS_SERVICE_URL=http://users-service:7001/api/v1

# --- Cache TTL ---
USER_CACHE_TTL=300
IDEMPOTENCY_TTL=86400

# --- Providers Email ---
SENDGRID_API_KEY=
MAILGUN_API_KEY=
MAILGUN_DOMAIN=
DEFAULT_FROM_EMAIL=noreply@agtechnologies.com

# --- Providers SMS ---
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=

# --- Push ---
FCM_SERVER_KEY=

# --- CORS ---
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\CDC_v1.0.md =====
`
# AGT Notification Service - Cahier des Charges v1.0

> Version : 1.0 | Statut : Implementation-ready | Classification : Confidentiel

## 1. Perimetre

Envoi multi-canal (email, SMS, push, in-app, WhatsApp), templates dynamiques Jinja2, campagnes, preferences utilisateur, notifications planifiees, device tokens.

## 2. Stack

| Composant | Technologie |
|-----------|-------------|
| Framework | Django 5.x + DRF |
| Workers | Celery 5.x |
| Broker | RabbitMQ 3.13 |
| Cache | Redis 7+ |
| Templates | Jinja2 |
| Doc API | drf-spectacular |

## 3. Modele de donnees

11 tables : notifications, notification_logs, user_preferences, scheduled_notifications, platform_channel_config, templates, template_versions, template_variables, campaigns, campaign_recipients, device_tokens.

## 4. Providers

| Canal | Provider 1 | Provider 2 |
|-------|-----------|-----------|
| Email | SendGrid | Mailgun |
| SMS | Twilio | Vonage |
| Push | FCM | - |
| WhatsApp | Meta Cloud API | - |

Strategie fallback : retry meme provider (3x backoff) > autre provider meme canal > fallback inter-canal (sauf security).

## 5. Endpoints

### Envoi
- `POST /notifications/send` - Envoi mono/multi-canal
- `POST /notifications/send-bulk` - Envoi masse (max 100)

### In-App
- `GET /users/{id}/notifications` - Lister
- `GET /users/{id}/notifications/unread-count` - Badge
- `PUT /users/{id}/notifications/{nId}/read` - Marquer lue
- `PUT /users/{id}/notifications/read-all` - Tout lire
- `DELETE /users/{id}/notifications/{nId}` - Supprimer

### Templates
- `POST/GET /templates` - CRUD
- `GET /templates/{id}` - Detail
- `PUT /templates/{id}` - Nouvelle version
- `POST /templates/{id}/preview` - Preview
- `GET /templates/{id}/versions` - Historique

### Campagnes
- `POST/GET /campaigns` - CRUD
- `GET /campaigns/{id}` - Detail
- `GET /campaigns/{id}/progress` - Progression
- `POST /campaigns/{id}/cancel` - Annuler

### Preferences
- `GET/PUT /users/{id}/notification-preferences`

### Device Tokens
- `POST/GET /users/{id}/device-tokens`
- `DELETE /users/{id}/device-tokens/{tId}`

### Config
- `GET/PUT /platforms/{id}/channels-priority`

## 6. Templates requis par Auth

| Nom | Canal | Variables |
|-----|-------|-----------|
| auth_verify_email | email | verification_url, expires_in_minutes, platform_name |
| auth_otp_sms | sms | otp_code, expires_in_minutes, platform_name |
| auth_reset_password | email | reset_url, expires_in_minutes, platform_name |
| auth_magic_link | email | magic_link_url, expires_in_minutes, platform_name |

## 7. Port

Service : **7002** | RabbitMQ Management : **15672**

---

*AG Technologies - Notification Service CDC v1.0 - Confidentiel*

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_notif_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: agt_notification_db
      POSTGRES_USER: notif_user
      POSTGRES_PASSWORD: notif_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5434:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U notif_user -d agt_notification_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: agt_notif_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb
    volumes:
      - redis_data:/data
    ports:
      - "6381:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    container_name: agt_notif_rabbitmq
    restart: unless-stopped
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 15s
      timeout: 10s
      retries: 5

  notification:
    build:
      context: .
      target: production
    container_name: agt_notif_service
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://notif_user:notif_password@db:5432/agt_notification_db
      REDIS_URL: redis://redis:6379/2
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672//
      CELERY_RESULT_BACKEND: redis://redis:6379/3
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7002:7002"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7002/api/v1/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  celery-worker:
    build:
      context: .
      target: production
    container_name: agt_notif_worker
    restart: unless-stopped
    command: celery -A config.celery worker -l info -c 4
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://notif_user:notif_password@db:5432/agt_notification_db
      REDIS_URL: redis://redis:6379/2
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672//
      CELERY_RESULT_BACKEND: redis://redis:6379/3
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy

  celery-beat:
    build:
      context: .
      target: production
    container_name: agt_notif_beat
    restart: unless-stopped
    command: celery -A config.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://notif_user:notif_password@db:5432/agt_notification_db
      REDIS_URL: redis://redis:6379/2
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672//
    depends_on:
      db:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy

  notification-dev:
    build:
      context: .
      target: builder
    container_name: agt_notif_dev
    restart: unless-stopped
    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py runserver 0.0.0.0:7002"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://notif_user:notif_password@db:5432/agt_notification_db
      REDIS_URL: redis://redis:6379/2
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672//
      DEBUG: "True"
      DJANGO_SETTINGS_MODULE: config.settings
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7002:7002"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    profiles:
      - dev

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7002
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7002", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\manage.py =====
`
#!/usr/bin/env python
import os, sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\README.md =====
`
# AGT Notification Service - v1.0

Service de notification multi-canal de l'ecosysteme AG Technologies.
Email, SMS, push, in-app, WhatsApp avec templates dynamiques et campagnes.

## Stack

| Composant | Technologie |
|-----------|-------------|
| Framework | Django 5.x + DRF |
| Workers | Celery 5.x |
| Broker | RabbitMQ 3.13 |
| Cache | Redis 7+ |
| Templates | Jinja2 |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## Prerequisites

- Docker 24+ et Docker Compose v2
- Cle publique RSA du Service Auth

## Demarrage rapide

### Linux / macOS

```bash
bash scripts/setup.sh
```

### Windows (PowerShell)

```powershell
# 1. Ouvrir Docker Desktop et attendre qu'il soit pret (icone verte)

# 2. Autoriser l'execution des scripts (une seule fois par session)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Lancer le setup
.\scripts\setup.ps1
```

> Le Service Auth doit etre demarre en premier pour generer les cles RSA.
> Le script copie automatiquement `../agt-auth/keys/public.pem`.

## Documentation API (Swagger)

| URL | Description |
|-----|-------------|
| http://localhost:7002/api/v1/docs/ | Swagger UI |
| http://localhost:7002/api/v1/redoc/ | ReDoc |
| http://localhost:15672 | RabbitMQ Management (guest/guest) |

## Services Docker

| Container | Role |
|-----------|------|
| notification | API Django (port 7002) |
| celery-worker | Worker async (envoi notifications) |
| celery-beat | Scheduler (notifications planifiees) |
| rabbitmq | Message broker |
| redis | Cache + result backend |
| db | PostgreSQL |

## Endpoints principaux

Base URL : `http://localhost:7002/api/v1`

### Envoi
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/notifications/send` | Envoi mono/multi-canal |
| POST | `/notifications/send-bulk` | Envoi masse (max 100) |

### In-App
| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users/{id}/notifications` | Lister |
| GET | `/users/{id}/notifications/unread-count` | Badge non lues |
| PUT | `/users/{id}/notifications/{nId}/read` | Marquer lue |
| PUT | `/users/{id}/notifications/read-all` | Tout lire |
| DELETE | `/users/{id}/notifications/{nId}` | Supprimer |

### Templates
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/templates` | CRUD |
| PUT | `/templates/{id}` | Nouvelle version |
| POST | `/templates/{id}/preview` | Preview avec variables |

### Campagnes
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/campaigns` | CRUD |
| GET | `/campaigns/{id}/progress` | Progression temps reel |
| POST | `/campaigns/{id}/cancel` | Annuler |

## Tests

```bash
docker compose exec notification python -m pytest -v
```

## Templates requis par Auth

Creer ces templates avant de demarrer Auth :

| Nom | Canal | Variables |
|-----|-------|-----------|
| auth_verify_email | email | verification_url, expires_in_minutes, platform_name |
| auth_otp_sms | sms | otp_code, expires_in_minutes, platform_name |
| auth_reset_password | email | reset_url, expires_in_minutes, platform_name |
| auth_magic_link | email | magic_link_url, expires_in_minutes, platform_name |

## Cahier des charges

Voir [CDC_v1.0.md](./CDC_v1.0.md)

## Dependances inter-services

| Service | Direction | Usage |
|---------|-----------|-------|
| **Auth** (7000) | Auth vers Notif | Envoi verifications, OTP, reset, magic link |
| **Users** (7001) | Notif vers Users | Resolution coordonnees (email/phone) |

---

*AG Technologies - Notification Service v1.0 - Confidentiel*

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\requirements.txt =====
`
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.4
celery==5.3.6
django-celery-beat==2.6.0
kombu==5.3.4
PyJWT==2.8.0
cryptography==42.0.5
drf-spectacular==0.27.2
sendgrid==6.11.0
twilio==9.0.5
httpx==0.27.0
Jinja2==3.1.4
python-decouple==3.8
python-json-logger==2.0.7
gunicorn==22.0.0
pytest==8.2.0
pytest-django==4.8.0
factory-boy==3.3.0
faker==25.0.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\models.py =====
`
"""AGT Notification Service v1.0 - Modeles : Campaign, CampaignRecipient."""
import uuid
from django.db import models


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    platform_id = models.UUIDField()
    template = models.ForeignKey("templates_mgr.Template", on_delete=models.SET_NULL, null=True, blank=True, related_name="campaigns")
    channel = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="draft", db_index=True)
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    throttle_per_second = models.IntegerField(default=10)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "campaigns"
        ordering = ["-created_at"]

    @property
    def progress_percent(self):
        if not self.total_recipients:
            return 0.0
        return round((self.sent_count + self.failed_count) / self.total_recipients * 100, 1)

    def cancel(self):
        self.status = "cancelled"
        self.save(update_fields=["status"])


class CampaignRecipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="recipients")
    user_id = models.UUIDField()
    notification = models.ForeignKey("notifications.Notification", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")
    variables = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "campaign_recipients"
        ordering = ["created_at"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\urls.py =====
`
from django.urls import path
from apps.campaigns.views import CampaignListCreateView, CampaignDetailView, CampaignProgressView, CampaignCancelView

urlpatterns = [
    path("campaigns", CampaignListCreateView.as_view(), name="campaigns-list"),
    path("campaigns/<uuid:campaign_id>", CampaignDetailView.as_view(), name="campaigns-detail"),
    path("campaigns/<uuid:campaign_id>/progress", CampaignProgressView.as_view(), name="campaigns-progress"),
    path("campaigns/<uuid:campaign_id>/cancel", CampaignCancelView.as_view(), name="campaigns-cancel"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\views.py =====
`
"""AGT Notification Service v1.0 - Views Campaigns."""
import logging
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.notifications.pagination import StandardPagination

logger = logging.getLogger(__name__)


class CampaignListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Creer une campagne")
    def post(self, request):
        from apps.templates_mgr.models import Template
        from workers.tasks import process_campaign_task
        data = request.data
        name, template_name, channel = data.get("name"), data.get("template_name"), data.get("channel", "email")
        user_ids = data.get("user_ids", [])
        platform_id = str(getattr(request.user, "platform_id", "") or "")

        if not all([name, template_name, channel, user_ids]):
            return Response({"detail": "name, template_name, channel et user_ids requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            template = Template.resolve(template_name, platform_id=platform_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)

        campaign = Campaign.objects.create(
            name=name, platform_id=platform_id or "00000000-0000-0000-0000-000000000000",
            template=template, channel=channel, total_recipients=len(user_ids),
            throttle_per_second=data.get("throttle_per_second", 10),
            created_by=getattr(request.user, "auth_user_id", None),
        )
        CampaignRecipient.objects.bulk_create([
            CampaignRecipient(campaign=campaign, user_id=uid, variables=data.get("variables", {}))
            for uid in user_ids
        ])
        process_campaign_task.delay(str(campaign.id))
        return Response({"id": str(campaign.id), "name": name, "status": "draft", "total_recipients": len(user_ids)}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Campaigns"], summary="Lister les campagnes")
    def get(self, request):
        qs = Campaign.objects.all()
        if request.GET.get("status"):
            qs = qs.filter(status=request.GET["status"])
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(c.id), "name": c.name, "status": c.status, "sent_count": c.sent_count, "total_recipients": c.total_recipients} for c in page]
        return paginator.get_paginated_response(data)


class CampaignDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Detail campagne")
    def get(self, request, campaign_id):
        try:
            c = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"detail": "Campagne introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": str(c.id), "name": c.name, "status": c.status, "total_recipients": c.total_recipients,
                         "sent_count": c.sent_count, "failed_count": c.failed_count, "progress": c.progress_percent})


class CampaignProgressView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Progression campagne")
    def get(self, request, campaign_id):
        try:
            c = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"detail": "Campagne introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"progress": c.progress_percent, "sent": c.sent_count, "failed": c.failed_count, "total": c.total_recipients, "status": c.status})


class CampaignCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Annuler une campagne")
    def post(self, request, campaign_id):
        try:
            c = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"detail": "Campagne introuvable."}, status=status.HTTP_404_NOT_FOUND)
        c.cancel()
        return Response({"message": "Campagne annulee.", "status": "cancelled"})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\campaigns\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\models.py =====
`
"""AGT Notification Service v1.0 - Modele DeviceToken (push FCM/APNs)."""
import uuid
from django.db import models


class DeviceToken(models.Model):
    DEVICE_TYPES = [("android", "Android"), ("ios", "iOS"), ("web", "Web")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    platform_id = models.UUIDField()
    token = models.TextField()
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    device_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_tokens"
        constraints = [models.UniqueConstraint(fields=["user_id", "token"], name="unique_user_token")]
        indexes = [models.Index(fields=["user_id", "is_active"])]

    @classmethod
    def deactivate_all_for_user(cls, user_id):
        return cls.objects.filter(user_id=user_id, is_active=True).update(is_active=False)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\urls.py =====
`
from django.urls import path
from apps.devices.views import DeviceTokenListCreateView, DeviceTokenDeleteView

urlpatterns = [
    path("users/<str:user_id>/device-tokens", DeviceTokenListCreateView.as_view(), name="device-tokens"),
    path("users/<str:user_id>/device-tokens/<uuid:token_id>", DeviceTokenDeleteView.as_view(), name="device-token-delete"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\views.py =====
`
"""AGT Notification Service v1.0 - Views Device Tokens."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.devices.models import DeviceToken


class DeviceTokenListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Devices"], summary="Enregistrer un device token")
    def post(self, request, user_id):
        token = request.data.get("token")
        device_type = request.data.get("device_type")
        platform_id = str(getattr(request.user, "platform_id", "") or "")
        if not token or not device_type:
            return Response({"detail": "token et device_type requis."}, status=status.HTTP_400_BAD_REQUEST)

        dt, created = DeviceToken.objects.update_or_create(
            user_id=user_id, token=token,
            defaults={"platform_id": platform_id, "device_type": device_type,
                       "device_name": request.data.get("device_name"), "is_active": True},
        )
        return Response({"id": str(dt.id), "device_type": dt.device_type, "created": created},
                         status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @extend_schema(tags=["Devices"], summary="Lister les devices d'un utilisateur")
    def get(self, request, user_id):
        tokens = DeviceToken.objects.filter(user_id=user_id, is_active=True)
        data = [{"id": str(t.id), "device_type": t.device_type, "device_name": t.device_name, "created_at": t.created_at.isoformat()} for t in tokens]
        return Response({"data": data})


class DeviceTokenDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Devices"], summary="Supprimer un device token")
    def delete(self, request, user_id, token_id):
        deleted, _ = DeviceToken.objects.filter(id=token_id, user_id=user_id).delete()
        if not deleted:
            return Response({"detail": "Token introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Device token supprime."})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\devices\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\authentication.py =====
`
"""AGT Notification Service v1.0 - Authentication JWT (cle publique Auth)."""
import logging, jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JWTPayload:
    def __init__(self, payload):
        self.payload = payload
        self.id = payload.get("sub")
        self.auth_user_id = payload.get("sub")
        self.platform_id = payload.get("platform_id")
        self.is_authenticated = True


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ", 1)[1]
        cache_key = f"jwt:{token[:32]}"
        cached = cache.get(cache_key)
        if cached:
            return JWTPayload(cached), cached
        public_key = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not public_key:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try:
            payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(cache_key, payload, timeout=30)
        return JWTPayload(payload), payload

    def authenticate_header(self, request):
        return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\exceptions.py =====
`
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        logger.exception("Unhandled exception", exc_info=exc)
        response = Response({"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Erreur interne."}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\models.py =====
`
"""
AGT Notification Service v1.0 - Modeles principaux.
"""
import uuid
from django.db import models
from django.utils import timezone


class ChannelChoice(models.TextChoices):
    EMAIL = "email", "Email"
    SMS = "sms", "SMS"
    PUSH = "push", "Push"
    IN_APP = "in_app", "In-App"
    WHATSAPP = "whatsapp", "WhatsApp"


class CategoryChoice(models.TextChoices):
    TRANSACTIONAL = "transactional", "Transactionnel"
    MARKETING = "marketing", "Marketing"
    SECURITY = "security", "Securite"


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    SENT = "sent", "Envoye"
    DELIVERED = "delivered", "Livre"
    READ = "read", "Lu"
    FAILED = "failed", "Echoue"


class PriorityChoice(models.TextChoices):
    LOW = "low", "Faible"
    NORMAL = "normal", "Normal"
    HIGH = "high", "Haute"
    CRITICAL = "critical", "Critique"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    platform_id = models.UUIDField(db_index=True)
    template = models.ForeignKey("templates_mgr.Template", on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    channel = models.CharField(max_length=20, choices=ChannelChoice.choices, db_index=True)
    category = models.CharField(max_length=30, choices=CategoryChoice.choices)
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=NotificationStatus.choices, default=NotificationStatus.PENDING, db_index=True)
    priority = models.CharField(max_length=10, choices=PriorityChoice.choices, default=PriorityChoice.NORMAL)
    metadata = models.JSONField(null=True, blank=True)
    idempotency_key = models.CharField(max_length=100, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["platform_id", "idempotency_key"], name="unique_platform_idempotency", condition=models.Q(idempotency_key__isnull=False))
        ]
        indexes = [models.Index(fields=["user_id", "channel"]), models.Index(fields=["user_id", "status"])]

    @property
    def is_read(self):
        return self.read_at is not None

    def mark_as_read(self):
        self.read_at = timezone.now()
        self.status = NotificationStatus.READ
        self.save(update_fields=["read_at", "status"])

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def mark_sent(self):
        self.status = NotificationStatus.SENT
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sent_at"])

    def mark_failed(self):
        self.status = NotificationStatus.FAILED
        self.save(update_fields=["status"])


class NotificationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="logs")
    channel = models.CharField(max_length=20, choices=ChannelChoice.choices)
    provider = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    attempt = models.IntegerField()
    error_message = models.TextField(null=True, blank=True)
    provider_message_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification_logs"
        ordering = ["-created_at"]


class UserPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    platform_id = models.UUIDField()
    channel_email = models.BooleanField(default=True)
    channel_sms = models.BooleanField(default=True)
    channel_push = models.BooleanField(default=True)
    channel_whatsapp = models.BooleanField(default=True)
    channel_in_app = models.BooleanField(default=True)
    cat_transactional = models.BooleanField(default=True)
    cat_marketing = models.BooleanField(default=False)
    cat_security = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_preferences"
        unique_together = [("user_id", "platform_id")]

    def is_channel_enabled(self, channel):
        return getattr(self, f"channel_{channel}", True)

    def is_category_enabled(self, category):
        if category == "security":
            return True
        return getattr(self, f"cat_{category}", True)


class ScheduledNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    platform_id = models.UUIDField()
    template = models.ForeignKey("templates_mgr.Template", on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.CharField(max_length=20, choices=ChannelChoice.choices)
    variables = models.JSONField(null=True, blank=True)
    scheduled_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, default="pending")
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "scheduled_notifications"
        ordering = ["scheduled_at"]


class PlatformChannelConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(unique=True)
    priority_order = models.JSONField(default=list)
    fallback_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_channel_config"

    DEFAULT_ORDER = ["email", "push", "in_app", "whatsapp", "sms"]

    @classmethod
    def get_for_platform(cls, platform_id):
        try:
            return cls.objects.get(platform_id=platform_id)
        except cls.DoesNotExist:
            return cls(platform_id=platform_id, priority_order=cls.DEFAULT_ORDER, fallback_enabled=True)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\pagination.py =====
`
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({"data": data, "page": self.page.number,
                         "limit": self.get_page_size(self.request), "total": self.page.paginator.count})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\services.py =====
`
"""AGT Notification Service v1.0 - Services : cache user, preferences, idempotency."""
import logging
import httpx
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class UserResolverService:
    @staticmethod
    def get_user(user_id):
        cache_key = f"user_coords:{user_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return None
        try:
            resp = httpx.get(f"{url}/users/by-auth/{user_id}", timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data, timeout=getattr(settings, "USER_CACHE_TTL", 300))
                return data
        except Exception as e:
            logger.error(f"User resolve failed: {e}")
        return None


class PreferenceService:
    @staticmethod
    def is_allowed(user_id, platform_id, channel, category):
        if category == "security":
            return True
        from apps.notifications.models import UserPreference
        try:
            pref = UserPreference.objects.get(user_id=user_id, platform_id=platform_id)
        except UserPreference.DoesNotExist:
            return category != "marketing"
        return pref.is_channel_enabled(channel) and pref.is_category_enabled(category)


class IdempotencyService:
    @staticmethod
    def check_and_register(platform_id, key):
        cache_key = f"idemp:{platform_id}:{key}"
        if cache.get(cache_key):
            return True
        cache.set(cache_key, True, timeout=getattr(settings, "IDEMPOTENCY_TTL", 86400))
        return False

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\urls.py =====
`
from django.urls import path
from apps.notifications.views import (
    HealthCheckView, SendNotificationView, SendBulkNotificationView,
    PreferenceView, InAppListView, InAppUnreadCountView, InAppMarkReadView,
    InAppMarkAllReadView, InAppDeleteView, NotificationStatsView,
    NotificationLogsView, ChannelConfigView,
)

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
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\views.py =====
`
"""AGT Notification Service v1.0 - Views principales."""
import logging
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.notifications.models import (
    Notification, NotificationLog, UserPreference, ScheduledNotification,
    PlatformChannelConfig, ChannelChoice, CategoryChoice, NotificationStatus,
)
from apps.notifications.pagination import StandardPagination
from apps.notifications.services import UserResolverService, PreferenceService, IdempotencyService

logger = logging.getLogger(__name__)
VALID_CHANNELS = [c.value for c in ChannelChoice]
VALID_CATEGORIES = [c.value for c in CategoryChoice]


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check")
    def get(self, request):
        db_ok = redis_ok = broker_ok = True
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
        try:
            from config.celery import app as celery_app
            broker_ok = celery_app.control.inspect(timeout=1).ping() is not None
        except Exception:
            broker_ok = False

        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "broker": "ok" if broker_ok else "degraded", "version": "1.0.0"}, status=code)


class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Send"], summary="Envoi mono ou multi-canal")
    def post(self, request):
        from workers.tasks import send_notification_task
        from apps.templates_mgr.models import Template

        data = request.data
        user_id = data.get("user_id")
        channels = data.get("channels", [])
        template_name = data.get("template_name")
        locale = data.get("locale", "fr")
        variables = data.get("variables", {})
        priority = data.get("priority", "normal")
        category = data.get("category", "transactional")
        idempotency_key = data.get("idempotency_key")
        platform_id = str(getattr(request.user, "platform_id", "") or "")

        if not user_id or not channels or not template_name:
            return Response({"detail": "user_id, channels et template_name requis."}, status=status.HTTP_400_BAD_REQUEST)
        if category not in VALID_CATEGORIES:
            return Response({"detail": f"Categorie invalide. Valeurs: {VALID_CATEGORIES}"}, status=status.HTTP_400_BAD_REQUEST)

        if idempotency_key and platform_id:
            if IdempotencyService.check_and_register(platform_id, idempotency_key):
                return Response({"detail": "Cle d'idempotence deja utilisee."}, status=status.HTTP_409_CONFLICT)

        try:
            template = Template.resolve(template_name, platform_id=platform_id)
        except Template.DoesNotExist:
            return Response({"detail": f"Template '{template_name}' introuvable."}, status=status.HTTP_404_NOT_FOUND)

        try:
            rendered = template.render(variables, locale=locale)
        except Exception as e:
            return Response({"detail": f"Erreur rendu template: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        for ch in channels:
            if ch not in VALID_CHANNELS:
                continue
            if not PreferenceService.is_allowed(user_id, platform_id, ch, category):
                continue

            notif = Notification.objects.create(
                user_id=user_id, platform_id=platform_id or "00000000-0000-0000-0000-000000000000",
                template=template, channel=ch, category=category, subject=rendered.get("subject"),
                body=rendered.get("body", ""), priority=priority,
                idempotency_key=idempotency_key if len(channels) == 1 else None,
                metadata={"variables": variables, "locale": locale},
            )
            send_notification_task.delay(str(notif.id))
            created.append({"id": str(notif.id), "channel": ch, "status": "pending"})

        return Response({"notifications": created, "message": "Notifications queued"}, status=status.HTTP_202_ACCEPTED)


class SendBulkNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Send"], summary="Envoi en masse (max 100)")
    def post(self, request):
        from workers.tasks import send_notification_task
        from apps.templates_mgr.models import Template

        data = request.data
        user_ids = data.get("user_ids", [])
        channels = data.get("channels", [])
        template_name = data.get("template_name")
        if not user_ids or not channels or not template_name:
            return Response({"detail": "user_ids, channels et template_name requis."}, status=status.HTTP_400_BAD_REQUEST)
        if len(user_ids) > 100:
            return Response({"detail": "Max 100 user_ids. Utilisez les campagnes pour plus."}, status=status.HTTP_400_BAD_REQUEST)

        platform_id = str(getattr(request.user, "platform_id", "") or "")
        try:
            template = Template.resolve(template_name, platform_id=platform_id)
        except Template.DoesNotExist:
            return Response({"detail": f"Template introuvable."}, status=status.HTTP_404_NOT_FOUND)

        variables = data.get("variables", {})
        locale = data.get("locale", "fr")
        category = data.get("category", "transactional")
        rendered = template.render(variables, locale=locale)

        total = 0
        for uid in user_ids:
            for ch in channels:
                notif = Notification.objects.create(
                    user_id=uid, platform_id=platform_id or "00000000-0000-0000-0000-000000000000",
                    template=template, channel=ch, category=category, subject=rendered.get("subject"),
                    body=rendered.get("body", ""), metadata={"variables": variables},
                )
                send_notification_task.delay(str(notif.id))
                total += 1

        return Response({"message": f"{total} notifications queued", "total": total}, status=status.HTTP_202_ACCEPTED)


class PreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Preferences"], summary="Lire les preferences")
    def get(self, request, user_id):
        try:
            pref = UserPreference.objects.get(user_id=user_id, platform_id=getattr(request.user, "platform_id", ""))
            return Response({
                "channels": {"email": pref.channel_email, "sms": pref.channel_sms, "push": pref.channel_push, "whatsapp": pref.channel_whatsapp, "in_app": pref.channel_in_app},
                "categories": {"transactional": pref.cat_transactional, "marketing": pref.cat_marketing, "security": True},
            })
        except UserPreference.DoesNotExist:
            return Response({"channels": {"email": True, "sms": True, "push": True, "whatsapp": True, "in_app": True},
                             "categories": {"transactional": True, "marketing": False, "security": True}})

    @extend_schema(tags=["Preferences"], summary="Modifier les preferences")
    def put(self, request, user_id):
        platform_id = str(getattr(request.user, "platform_id", "") or "")
        pref, _ = UserPreference.objects.get_or_create(user_id=user_id, platform_id=platform_id)
        channels = request.data.get("channels", {})
        categories = request.data.get("categories", {})
        for ch in ["email", "sms", "push", "whatsapp", "in_app"]:
            if ch in channels:
                setattr(pref, f"channel_{ch}", channels[ch])
        for cat in ["transactional", "marketing"]:
            if cat in categories:
                setattr(pref, f"cat_{cat}", categories[cat])
        pref.save()
        return Response({"message": "Preferences mises a jour."})


class InAppListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Lister notifications in-app")
    def get(self, request, user_id):
        qs = Notification.objects.filter(user_id=user_id, channel="in_app", deleted_at__isnull=True)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(n.id), "subject": n.subject, "body": n.body, "is_read": n.is_read,
                 "created_at": n.created_at.isoformat()} for n in page]
        return paginator.get_paginated_response(data)


class InAppUnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Compteur non lues (badge)")
    def get(self, request, user_id):
        count = Notification.objects.filter(user_id=user_id, channel="in_app", read_at__isnull=True, deleted_at__isnull=True).count()
        return Response({"user_id": str(user_id), "unread_count": count})


class InAppMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Marquer comme lue")
    def put(self, request, user_id, notification_id):
        try:
            notif = Notification.objects.get(id=notification_id, user_id=user_id, channel="in_app")
        except Notification.DoesNotExist:
            return Response({"detail": "Notification introuvable."}, status=status.HTTP_404_NOT_FOUND)
        notif.mark_as_read()
        return Response({"message": "Notification lue."})


class InAppMarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Tout marquer comme lu")
    def put(self, request, user_id):
        updated = Notification.objects.filter(user_id=user_id, channel="in_app", read_at__isnull=True).update(
            read_at=timezone.now(), status=NotificationStatus.READ)
        return Response({"message": f"{updated} notifications marquees lues."})


class InAppDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Supprimer notification in-app")
    def delete(self, request, user_id, notification_id):
        try:
            notif = Notification.objects.get(id=notification_id, user_id=user_id, channel="in_app")
        except Notification.DoesNotExist:
            return Response({"detail": "Notification introuvable."}, status=status.HTTP_404_NOT_FOUND)
        notif.soft_delete()
        return Response({"message": "Notification supprimee."})


class NotificationStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Stats"], summary="Statistiques globales")
    def get(self, request):
        by_status = dict(Notification.objects.values_list("status").annotate(c=Count("id")))
        by_channel = dict(Notification.objects.values_list("channel").annotate(c=Count("id")))
        return Response({"by_status": by_status, "by_channel": by_channel})


class NotificationLogsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Stats"], summary="Logs d'envoi")
    def get(self, request):
        qs = NotificationLog.objects.all()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(l.id), "notification_id": str(l.notification_id), "channel": l.channel,
                 "provider": l.provider, "status": l.status, "attempt": l.attempt,
                 "created_at": l.created_at.isoformat()} for l in page]
        return paginator.get_paginated_response(data)


class ChannelConfigView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Config"], summary="Config canaux plateforme")
    def get(self, request, platform_id):
        config = PlatformChannelConfig.get_for_platform(str(platform_id))
        return Response({"platform_id": str(platform_id), "priority_order": config.priority_order, "fallback_enabled": config.fallback_enabled})

    @extend_schema(tags=["Config"], summary="Modifier config canaux")
    def put(self, request, platform_id):
        config, _ = PlatformChannelConfig.objects.get_or_create(platform_id=platform_id, defaults={"priority_order": PlatformChannelConfig.DEFAULT_ORDER})
        if "priority_order" in request.data:
            config.priority_order = request.data["priority_order"]
        if "fallback_enabled" in request.data:
            config.fallback_enabled = request.data["fallback_enabled"]
        config.save()
        return Response({"message": "Config mise a jour."})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\tests\test_all.py =====
`
"""AGT Notification Service v1.0 - Tests."""
import uuid
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

from apps.notifications.models import Notification, UserPreference, PlatformChannelConfig
from apps.templates_mgr.models import Template, TemplateVersion
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.devices.models import DeviceToken


def make_template(name="test_tpl", channel="email", body="Hello {{ name }}", platform_id=None):
    tpl = Template.objects.create(name=name, channel=channel, platform_id=platform_id, category="transactional")
    TemplateVersion.objects.create(template=tpl, version=1, locale="fr", subject="Test", body=body, is_current=True)
    return tpl


class TestModels(TestCase):
    def test_notification_lifecycle(self):
        n = Notification.objects.create(user_id=uuid.uuid4(), platform_id=uuid.uuid4(),
                                         channel="email", category="transactional", body="Test")
        self.assertEqual(n.status, "pending")
        n.mark_sent()
        n.refresh_from_db()
        self.assertEqual(n.status, "sent")

    def test_notification_in_app(self):
        n = Notification.objects.create(user_id=uuid.uuid4(), platform_id=uuid.uuid4(),
                                         channel="in_app", category="transactional", body="Test")
        self.assertFalse(n.is_read)
        n.mark_as_read()
        self.assertTrue(n.is_read)

    def test_template_resolve_platform_then_global(self):
        pid = uuid.uuid4()
        make_template(name="order", platform_id=pid)
        make_template(name="order", platform_id=None, body="Global {{ name }}")
        tpl = Template.resolve("order", platform_id=str(pid))
        self.assertEqual(tpl.platform_id, pid)

    def test_template_resolve_fallback_global(self):
        make_template(name="global_tpl", platform_id=None)
        tpl = Template.resolve("global_tpl", platform_id=str(uuid.uuid4()))
        self.assertIsNone(tpl.platform_id)

    def test_template_render(self):
        tpl = make_template(body="Bonjour {{ name }}")
        result = tpl.render({"name": "Jean"})
        self.assertEqual(result["body"], "Bonjour Jean")

    def test_preference_defaults(self):
        pref = UserPreference()
        self.assertTrue(pref.is_channel_enabled("email"))
        self.assertTrue(pref.is_category_enabled("security"))
        self.assertFalse(pref.cat_marketing)

    def test_device_token(self):
        uid = uuid.uuid4()
        DeviceToken.objects.create(user_id=uid, platform_id=uuid.uuid4(), token="fcm123", device_type="android")
        self.assertEqual(DeviceToken.objects.filter(user_id=uid).count(), 1)

    def test_campaign_progress(self):
        c = Campaign.objects.create(name="Test", platform_id=uuid.uuid4(), channel="email", total_recipients=100, sent_count=50)
        self.assertEqual(c.progress_percent, 50.0)


class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        resp = client.get("/api/v1/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestSendEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    @patch("workers.tasks.send_notification_task.delay")
    def test_send_notification(self, mock_task):
        tpl = make_template(name="test_send")
        resp = self.client.post("/api/v1/notifications/send", data={
            "user_id": str(uuid.uuid4()), "channels": ["email"],
            "template_name": "test_send", "variables": {"name": "Test"},
        }, format="json")
        self.assertEqual(resp.status_code, 202)
        self.assertTrue(mock_task.called)

    def test_send_missing_fields(self):
        resp = self.client.post("/api/v1/notifications/send", data={}, format="json")
        self.assertEqual(resp.status_code, 400)

    @patch("workers.tasks.send_notification_task.delay")
    def test_idempotency(self, mock_task):
        tpl = make_template(name="idemp_test")
        data = {"user_id": str(uuid.uuid4()), "channels": ["email"],
                "template_name": "idemp_test", "idempotency_key": "key123"}
        self.client.post("/api/v1/notifications/send", data=data, format="json")
        resp2 = self.client.post("/api/v1/notifications/send", data=data, format="json")
        self.assertEqual(resp2.status_code, 409)


class TestTemplateEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": None, "auth_user_id": str(uuid.uuid4())})())

    def test_create_template(self):
        resp = self.client.post("/api/v1/templates", data={
            "name": "new_tpl", "channel": "email", "body": "Hello {{ name }}",
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_templates(self):
        make_template()
        resp = self.client.get("/api/v1/templates")
        self.assertEqual(resp.status_code, 200)


class TestInApp(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uid = str(uuid.uuid4())
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": None, "auth_user_id": self.uid})())

    def test_unread_count(self):
        Notification.objects.create(user_id=self.uid, platform_id=uuid.uuid4(), channel="in_app", category="transactional", body="Test")
        resp = self.client.get(f"/api/v1/users/{self.uid}/notifications/unread-count")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["unread_count"], 1)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\notifications\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\models.py =====
`
"""
AGT Notification Service v1.0 - Modeles : Template, TemplateVersion, TemplateVariable.
"""
import uuid
from django.db import models


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=20)
    platform_id = models.UUIDField(null=True, blank=True, db_index=True)
    category = models.CharField(max_length=30, default="transactional")
    is_active = models.BooleanField(default=True)
    created_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "templates"
        constraints = [models.UniqueConstraint(fields=["name", "platform_id"], name="unique_template_name_platform")]
        ordering = ["name"]

    def get_current_version(self, locale="fr"):
        version = self.versions.filter(is_current=True, locale=locale).first()
        if not version and locale != "fr":
            version = self.versions.filter(is_current=True, locale="fr").first()
        return version

    def render(self, variables, locale="fr"):
        from jinja2 import Environment
        version = self.get_current_version(locale)
        if not version:
            raise ValueError(f"Aucune version active pour '{self.name}' (locale: {locale})")
        env = Environment()
        subject = env.from_string(version.subject or "").render(**variables) if version.subject else None
        body = env.from_string(version.body).render(**variables)
        return {"subject": subject, "body": body}

    @classmethod
    def resolve(cls, name, platform_id=None, channel=None):
        qs = cls.objects.filter(name=name, is_active=True)
        if platform_id:
            tpl = qs.filter(platform_id=platform_id).first()
            if tpl:
                return tpl
        tpl = qs.filter(platform_id__isnull=True).first()
        if tpl:
            return tpl
        raise cls.DoesNotExist(f"Template '{name}' introuvable")


class TemplateVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="versions")
    version = models.IntegerField()
    locale = models.CharField(max_length=10, default="fr")
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "template_versions"
        ordering = ["-version"]
        unique_together = [("template", "version", "locale")]


class TemplateVariable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=False)
    default_value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "template_variables"
        unique_together = [("template", "name")]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\urls.py =====
`
from django.urls import path
from apps.templates_mgr.views import TemplateListCreateView, TemplateDetailView, TemplatePreviewView, TemplateVersionsView

urlpatterns = [
    path("templates", TemplateListCreateView.as_view(), name="templates-list"),
    path("templates/<uuid:template_id>", TemplateDetailView.as_view(), name="templates-detail"),
    path("templates/<uuid:template_id>/preview", TemplatePreviewView.as_view(), name="templates-preview"),
    path("templates/<uuid:template_id>/versions", TemplateVersionsView.as_view(), name="templates-versions"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\views.py =====
`
"""AGT Notification Service v1.0 - Views Templates CRUD."""
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.templates_mgr.models import Template, TemplateVersion
from apps.notifications.pagination import StandardPagination

logger = logging.getLogger(__name__)


class TemplateListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Creer un template")
    def post(self, request):
        data = request.data
        name, channel, body = data.get("name"), data.get("channel"), data.get("body", "")
        platform_id = data.get("platform_id")
        if not all([name, channel, body]):
            return Response({"detail": "name, channel et body requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Template.objects.filter(name=name, platform_id=platform_id).exists():
            return Response({"detail": f"Template '{name}' existe deja."}, status=status.HTTP_409_CONFLICT)

        tpl = Template.objects.create(name=name, channel=channel, platform_id=platform_id,
                                       category=data.get("category", "transactional"),
                                       created_by=getattr(request.user, "auth_user_id", None))
        TemplateVersion.objects.create(template=tpl, version=1, locale=data.get("locale", "fr"),
                                        subject=data.get("subject"), body=body, is_current=True)
        return Response({"id": str(tpl.id), "name": tpl.name, "channel": tpl.channel}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Templates"], summary="Lister les templates")
    def get(self, request):
        qs = Template.objects.filter(is_active=True)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(t.id), "name": t.name, "channel": t.channel, "platform_id": str(t.platform_id) if t.platform_id else None, "category": t.category} for t in page]
        return paginator.get_paginated_response(data)


class TemplateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Detail template")
    def get(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)
        version = tpl.get_current_version()
        return Response({"id": str(tpl.id), "name": tpl.name, "channel": tpl.channel,
                         "subject": version.subject if version else None, "body": version.body if version else ""})

    @extend_schema(tags=["Templates"], summary="Modifier template (nouvelle version)")
    def put(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        last_version = tpl.versions.order_by("-version").first()
        new_version_num = (last_version.version + 1) if last_version else 1
        tpl.versions.filter(is_current=True).update(is_current=False)
        TemplateVersion.objects.create(template=tpl, version=new_version_num, locale=data.get("locale", "fr"),
                                        subject=data.get("subject"), body=data.get("body", ""), is_current=True)
        tpl.save()
        return Response({"message": "Template mis a jour.", "version": new_version_num})

    @extend_schema(tags=["Templates"], summary="Desactiver template")
    def delete(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)
        tpl.is_active = False
        tpl.save(update_fields=["is_active"])
        return Response({"message": "Template desactive."})


class TemplatePreviewView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Preview avec variables")
    def post(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)
        variables = request.data.get("variables", {})
        locale = request.data.get("locale", "fr")
        try:
            rendered = tpl.render(variables, locale=locale)
            return Response(rendered)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TemplateVersionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Historique versions")
    def get(self, request, template_id):
        versions = TemplateVersion.objects.filter(template_id=template_id)
        data = [{"version": v.version, "locale": v.locale, "is_current": v.is_current, "created_at": v.created_at.isoformat()} for v in versions]
        return Response({"data": data})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\apps\templates_mgr\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\celery.py =====
`
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("agt_notification")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\settings.py =====
`
"""AGT Notification Service v1.0 - Django Settings"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes", "django.contrib.staticfiles",
    "django_celery_beat", "rest_framework", "drf_spectacular", "corsheaders",
    "apps.notifications", "apps.templates_mgr", "apps.campaigns", "apps.devices",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
              "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]

import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/2")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL,
                       "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}

CELERY_BROKER_URL = config("RABBITMQ_URL", default=config("CELERY_BROKER_URL", default="amqp://guest:guest@localhost:5672//"))
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/3")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_ACKS_LATE = True

def _read_key(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
AUTH_SERVICE_URL = config("AUTH_SERVICE_URL", default="")
USERS_SERVICE_URL = config("USERS_SERVICE_URL", default="")
USER_CACHE_TTL = config("USER_CACHE_TTL", default=300, cast=int)
IDEMPOTENCY_TTL = config("IDEMPOTENCY_TTL", default=86400, cast=int)

SENDGRID_API_KEY = config("SENDGRID_API_KEY", default="")
MAILGUN_API_KEY = config("MAILGUN_API_KEY", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@agtechnologies.com")
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default="")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default="")
TWILIO_FROM_NUMBER = config("TWILIO_FROM_NUMBER", default="")
FCM_SERVER_KEY = config("FCM_SERVER_KEY", default="")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["apps.notifications.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.notifications.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.notifications.pagination.StandardPagination",
    "PAGE_SIZE": 20, "UNAUTHENTICATED_USER": None,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Notification Service API", "VERSION": "1.0.0",
    "DESCRIPTION": "Envoi multi-canal, templates dynamiques, campagnes, preferences, in-app.",
    "TAGS": [
        {"name": "Health"}, {"name": "Send", "description": "Envoi notifications"},
        {"name": "Templates"}, {"name": "Campaigns"}, {"name": "Preferences"},
        {"name": "In-App"}, {"name": "Devices"}, {"name": "Stats"}, {"name": "Config"},
    ],
}

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {"version": 1, "disable_existing_loggers": False,
           "handlers": {"console": {"class": "logging.StreamHandler"}},
           "root": {"handlers": ["console"], "level": "INFO"}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\settings_test.py =====
`
from config.settings import *  # noqa
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
AUTH_PRIVATE_KEY_FOR_TEST = _k.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()).decode()

AUTH_SERVICE_URL = ""
USERS_SERVICE_URL = ""
SENDGRID_API_KEY = ""
TWILIO_ACCOUNT_SID = ""
FCM_SERVER_KEY = ""
LOGGING = {"version": 1, "disable_existing_loggers": True, "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("api/v1/", include("apps.notifications.urls")),
    path("api/v1/", include("apps.templates_mgr.urls")),
    path("api/v1/", include("apps.campaigns.urls")),
    path("api/v1/", include("apps.devices.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\providers\providers.py =====
`
"""AGT Notification Service v1.0 - Providers abstraction layer."""
import logging
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class SendResult:
    success: bool
    error: str = None
    provider_message_id: str = None


class BaseProvider:
    name = "base"

    def send(self, notification, user_data):
        raise NotImplementedError


class SendGridProvider(BaseProvider):
    name = "sendgrid"

    def send(self, notification, user_data):
        from django.conf import settings
        api_key = getattr(settings, "SENDGRID_API_KEY", "")
        if not api_key:
            logger.warning("SENDGRID_API_KEY non configure")
            return False
        email = (user_data or {}).get("email")
        if not email:
            return False
        try:
            import httpx
            resp = httpx.post("https://api.sendgrid.com/v3/mail/send", headers={
                "Authorization": f"Bearer {api_key}", "Content-Type": "application/json"
            }, json={
                "personalizations": [{"to": [{"email": email}]}],
                "from": {"email": getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@agt.com")},
                "subject": notification.subject or "Notification",
                "content": [{"type": "text/html", "value": notification.body}],
            }, timeout=10.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"SendGrid error: {e}")
            return False


class MailgunProvider(BaseProvider):
    name = "mailgun"

    def send(self, notification, user_data):
        logger.info(f"[MOCK] Mailgun send to {(user_data or {}).get('email')}")
        return False  # Fallback provider - implement when needed


class TwilioProvider(BaseProvider):
    name = "twilio"

    def send(self, notification, user_data):
        from django.conf import settings
        sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
        token = getattr(settings, "TWILIO_AUTH_TOKEN", "")
        from_number = getattr(settings, "TWILIO_FROM_NUMBER", "")
        phone = (user_data or {}).get("phone")
        if not all([sid, token, from_number, phone]):
            return False
        try:
            import httpx
            resp = httpx.post(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
                              auth=(sid, token), data={
                                  "From": from_number, "To": phone, "Body": notification.body,
                              }, timeout=10.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Twilio error: {e}")
            return False


class VonageProvider(BaseProvider):
    name = "vonage"

    def send(self, notification, user_data):
        logger.info(f"[MOCK] Vonage send to {(user_data or {}).get('phone')}")
        return False


class FCMProvider(BaseProvider):
    name = "fcm"

    def send(self, notification, user_data):
        from django.conf import settings
        server_key = getattr(settings, "FCM_SERVER_KEY", "")
        if not server_key:
            return False
        from apps.devices.models import DeviceToken
        tokens = DeviceToken.objects.filter(user_id=notification.user_id, is_active=True, device_type__in=["android", "web"]).values_list("token", flat=True)
        if not tokens:
            return False
        try:
            import httpx
            for t in tokens:
                httpx.post("https://fcm.googleapis.com/fcm/send", headers={
                    "Authorization": f"key={server_key}", "Content-Type": "application/json"
                }, json={
                    "to": t, "notification": {"title": notification.subject or "Notification", "body": notification.body[:200]},
                }, timeout=10.0)
            return True
        except Exception as e:
            logger.error(f"FCM error: {e}")
            return False


class WhatsAppProvider(BaseProvider):
    name = "meta_whatsapp"

    def send(self, notification, user_data):
        logger.info(f"[MOCK] WhatsApp send to {(user_data or {}).get('phone')}")
        return False


PROVIDER_MAP = {
    "email": [SendGridProvider(), MailgunProvider()],
    "sms": [TwilioProvider(), VonageProvider()],
    "push": [FCMProvider()],
    "whatsapp": [WhatsAppProvider()],
    "in_app": [],
}


def get_providers(channel) -> List[BaseProvider]:
    return PROVIDER_MAP.get(channel, [])

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\providers\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\workers\tasks.py =====
`
"""AGT Notification Service v1.0 - Workers Celery : envoi, campagnes, scheduled."""
import logging
import time
import re
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=1, retry_backoff=True, name="notifications.send_notification")
def send_notification_task(self, notification_id):
    from apps.notifications.models import Notification, NotificationLog
    from apps.notifications.services import UserResolverService
    from providers.providers import get_providers

    try:
        notif = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    if notif.status != "pending":
        return

    user_data = UserResolverService.get_user(str(notif.user_id))
    if user_data and user_data.get("status") == "deleted":
        notif.mark_failed()
        return

    if notif.channel == "in_app":
        notif.mark_sent()
        return

    providers = get_providers(notif.channel)
    for attempt, provider in enumerate(providers, 1):
        try:
            success = provider.send(notif, user_data)
            NotificationLog.objects.create(notification=notif, channel=notif.channel, provider=provider.name,
                                            status="sent" if success else "failed", attempt=attempt)
            if success:
                notif.mark_sent()
                return
        except Exception as e:
            NotificationLog.objects.create(notification=notif, channel=notif.channel, provider=provider.name,
                                            status="failed", attempt=attempt, error_message=_mask(str(e)))

    if notif.category != "security":
        _try_fallback(notif, user_data)
    else:
        notif.mark_failed()


def _try_fallback(notif, user_data):
    from apps.notifications.models import PlatformChannelConfig, Notification
    from providers.providers import get_providers

    config = PlatformChannelConfig.get_for_platform(str(notif.platform_id))
    if not config.fallback_enabled:
        notif.mark_failed()
        return

    order = config.priority_order
    idx = order.index(notif.channel) if notif.channel in order else -1
    for ch in order[idx + 1:]:
        if ch == "in_app":
            Notification.objects.create(user_id=notif.user_id, platform_id=notif.platform_id, template=notif.template,
                                         channel="in_app", category=notif.category, subject=notif.subject,
                                         body=notif.body, status="sent", sent_at=timezone.now())
            notif.mark_failed()
            return
        for provider in get_providers(ch):
            try:
                if provider.send(notif, user_data):
                    notif.channel = ch
                    notif.mark_sent()
                    return
            except Exception:
                pass
    notif.mark_failed()


@shared_task(name="notifications.process_campaign")
def process_campaign_task(campaign_id):
    from apps.campaigns.models import Campaign, CampaignRecipient
    from apps.notifications.models import Notification

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return

    if campaign.status == "cancelled":
        return

    campaign.status = "running"
    campaign.started_at = timezone.now()
    campaign.save(update_fields=["status", "started_at"])

    recipients = CampaignRecipient.objects.filter(campaign=campaign, status="pending")
    delay = 1.0 / campaign.throttle_per_second if campaign.throttle_per_second > 0 else 0.1

    for r in recipients:
        campaign.refresh_from_db()
        if campaign.status == "cancelled":
            break
        try:
            rendered = campaign.template.render(r.variables or {}) if campaign.template else {"subject": None, "body": ""}
            notif = Notification.objects.create(user_id=r.user_id, platform_id=campaign.platform_id,
                                                 template=campaign.template, channel=campaign.channel,
                                                 category="marketing", subject=rendered.get("subject"),
                                                 body=rendered.get("body", ""), status="pending")
            r.notification = notif
            r.status = "sent"
            r.save(update_fields=["notification", "status"])
            send_notification_task.delay(str(notif.id))
            campaign.sent_count += 1
        except Exception as e:
            r.status = "failed"
            r.save(update_fields=["status"])
            campaign.failed_count += 1
        campaign.save(update_fields=["sent_count", "failed_count"])
        time.sleep(delay)

    if campaign.status != "cancelled":
        campaign.status = "completed"
        campaign.completed_at = timezone.now()
        campaign.save(update_fields=["status", "completed_at"])


@shared_task(name="notifications.process_scheduled")
def process_scheduled_notifications():
    from apps.notifications.models import ScheduledNotification, Notification
    now = timezone.now()
    pending = ScheduledNotification.objects.filter(status="pending", scheduled_at__lte=now)
    for sn in pending:
        try:
            rendered = sn.template.render(sn.variables or {}) if sn.template else {"subject": None, "body": ""}
            notif = Notification.objects.create(user_id=sn.user_id, platform_id=sn.platform_id,
                                                 template=sn.template, channel=sn.channel,
                                                 category="transactional", subject=rendered.get("subject"),
                                                 body=rendered.get("body", ""), status="pending")
            sn.notification = notif
            sn.status = "sent"
            sn.save(update_fields=["notification", "status", "updated_at"])
            send_notification_task.delay(str(notif.id))
        except Exception as e:
            logger.error(f"Scheduled {sn.id} failed: {e}")


def _mask(text):
    if not text:
        return text
    text = re.sub(r'[\w.-]+@[\w.-]+\.\w+', '[EMAIL]', text)
    text = re.sub(r'\+?[0-9]{8,15}', '[PHONE]', text)
    return text[:500]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-notification\workers\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\.env =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://pay_user:pay_password@db:5432/agt_payment_db
REDIS_URL=redis://redis:6379/5
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\.env.example =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://pay_user:pay_password@db:5432/agt_payment_db
REDIS_URL=redis://redis:6379/5
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\CDC_v1.0.md =====
`
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

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_pay_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: agt_payment_db
      POSTGRES_USER: pay_user
      POSTGRES_PASSWORD: pay_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5436:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pay_user -d agt_payment_db"]
      interval: 10s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    container_name: agt_pay_redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    ports:
      - "6383:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  payment:
    build:
      context: .
      target: production
    container_name: agt_pay_service
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://pay_user:pay_password@db:5432/agt_payment_db
      REDIS_URL: redis://redis:6379/5
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7005:7005"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7005/api/v1/payments/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  payment-dev:
    build:
      context: .
      target: builder
    container_name: agt_pay_dev
    command: sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:7005"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://pay_user:pay_password@db:5432/agt_payment_db
      REDIS_URL: redis://redis:6379/5
      DEBUG: "True"
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7005:7005"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles:
      - dev
volumes:
  postgres_data:
  redis_data:

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7005
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7005", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\manage.py =====
`
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == "__main__": main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\README.md =====
`
# AGT Payment Service - v1.0

Execution de transactions multi-provider: Orange Money, MTN MoMo, Stripe, PayPal.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
# Ouvrir Docker Desktop
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Documentation API

| URL | Description |
|-----|-------------|
| http://localhost:7005/api/v1/docs/ | Swagger UI |
| http://localhost:7005/api/v1/redoc/ | ReDoc |

## Tests
```bash
docker compose exec payment python -m pytest -v
```

## Endpoints

### Payments
- POST /payments/initiate (idempotency_key obligatoire)
- GET /payments (listing avec filtres)
- GET /payments/{id} (detail + historique statuts)
- POST /payments/{id}/cancel (pending uniquement)

### Webhooks (sans auth)
- POST /payments/webhooks/orange-money
- POST /payments/webhooks/mtn-momo
- POST /payments/webhooks/stripe
- POST /payments/webhooks/paypal

### Providers
- POST/GET /payments/providers (config globale)
- GET/PUT /payments/platforms/{id}/providers (config plateforme)

### Admin
- GET /payments/admin/stats
- POST /payments/admin/{id}/force-status

Voir [CDC_v1.0.md](./CDC_v1.0.md)

Port : **7005**

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\requirements.txt =====
`
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.4
PyJWT==2.8.0
cryptography==42.0.5
drf-spectacular==0.27.2
python-decouple==3.8
httpx==0.27.0
gunicorn==22.0.0
pytest==8.2.0
pytest-django==4.8.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\models.py =====
`
"""AGT Payment Service v1.0 - Modeles."""
import uuid
from django.db import models
from django.utils import timezone


class TransactionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


TERMINAL_STATUSES = {TransactionStatus.SUCCEEDED, TransactionStatus.FAILED, TransactionStatus.EXPIRED, TransactionStatus.CANCELLED}

VALID_TRANSITIONS = {
    None: {TransactionStatus.PENDING},
    TransactionStatus.PENDING: {TransactionStatus.PROCESSING, TransactionStatus.SUCCEEDED, TransactionStatus.FAILED, TransactionStatus.EXPIRED, TransactionStatus.CANCELLED},
    TransactionStatus.PROCESSING: {TransactionStatus.SUCCEEDED, TransactionStatus.FAILED, TransactionStatus.EXPIRED},
}


class Transaction(models.Model):
    PROVIDER_CHOICES = [("orange_money", "Orange Money"), ("mtn_momo", "MTN MoMo"), ("stripe", "Stripe"), ("paypal", "PayPal")]
    SOURCE_CHOICES = [("subscription", "Subscription"), ("wallet", "Wallet"), ("platform_direct", "Platform Direct")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    provider_tx_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    idempotency_key = models.UUIDField(unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.PENDING, db_index=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES)
    source_reference_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    payment_url = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    provider_raw_status = models.CharField(max_length=50, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["platform_id", "status"]), models.Index(fields=["source", "source_reference_id"])]

    def can_transition_to(self, new_status):
        allowed = VALID_TRANSITIONS.get(self.status, set())
        return new_status in allowed

    def transition_to(self, new_status, trigger="system", metadata=None):
        if not self.can_transition_to(new_status):
            raise ValueError(f"Transition {self.status} -> {new_status} interdite")
        old = self.status
        self.status = new_status
        if new_status == TransactionStatus.SUCCEEDED:
            self.confirmed_at = timezone.now()
        updates = ["status", "updated_at"]
        if self.confirmed_at:
            updates.append("confirmed_at")
        self.save(update_fields=updates)
        TransactionStatusHistory.objects.create(transaction=self, from_status=old, to_status=new_status, trigger=trigger, metadata=metadata)

    def is_terminal(self):
        return self.status in TERMINAL_STATUSES


class TransactionStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="status_history")
    from_status = models.CharField(max_length=20, null=True, blank=True)
    to_status = models.CharField(max_length=20)
    trigger = models.CharField(max_length=30, default="system")
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction_status_history"
        ordering = ["created_at"]


class WebhookLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=30)
    event_id = models.CharField(max_length=255, null=True, blank=True)
    payload = models.JSONField()
    headers = models.JSONField(null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name="webhook_logs")
    processed = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "webhook_logs"
        ordering = ["-created_at"]


class ProviderConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=100)
    credentials_encrypted = models.JSONField(default=dict)
    api_base_url = models.TextField(null=True, blank=True)
    webhook_secret_encrypted = models.CharField(max_length=500, null=True, blank=True)
    supported_currencies = models.JSONField(default=list)
    config = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provider_configs"


class PlatformPaymentConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(unique=True)
    providers_priority = models.JSONField(default=list)
    default_currency = models.CharField(max_length=3, default="XAF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_payment_config"

    @classmethod
    def get_for_platform(cls, platform_id):
        try:
            return cls.objects.get(platform_id=platform_id)
        except cls.DoesNotExist:
            return cls(platform_id=platform_id, providers_priority=["orange_money", "stripe"], default_currency="XAF")

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\service.py =====
`
"""AGT Payment Service v1.0 - Payment initiation and lifecycle."""
import logging
import uuid
from datetime import timedelta
from django.utils import timezone
from apps.payments.models import Transaction, TransactionStatus, WebhookLog

logger = logging.getLogger(__name__)

PROVIDER_TTL = {"orange_money": 300, "mtn_momo": 300, "stripe": 1800, "paypal": 3600}


class PaymentService:

    @classmethod
    def initiate(cls, platform_id, user_id, provider, amount, currency, source, source_reference_id, idempotency_key, phone_number=None, metadata=None):
        # Idempotency
        existing = Transaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        ttl = PROVIDER_TTL.get(provider, 600)
        tx = Transaction.objects.create(
            platform_id=platform_id, user_id=user_id, provider=provider,
            idempotency_key=idempotency_key, amount=amount, currency=currency,
            source=source, source_reference_id=source_reference_id,
            phone_number=phone_number, metadata=metadata,
            expires_at=timezone.now() + timedelta(seconds=ttl),
        )

        # Appeler le provider
        from apps.providers.adapters import get_adapter
        adapter = get_adapter(provider)
        if not adapter:
            tx.transition_to(TransactionStatus.FAILED, trigger="system", metadata={"reason": "provider_not_found"})
            return tx, "provider_not_found"

        try:
            result = adapter.initiate_payment(tx)
            if result.get("payment_url"):
                tx.payment_url = result["payment_url"]
                tx.save(update_fields=["payment_url"])
            if result.get("provider_tx_id"):
                tx.provider_tx_id = result["provider_tx_id"]
                tx.save(update_fields=["provider_tx_id"])
        except Exception as e:
            logger.error(f"Provider {provider} initiation failed: {e}")
            tx.transition_to(TransactionStatus.FAILED, trigger="provider_error", metadata={"error": str(e)[:200]})
            return tx, "provider_error"

        return tx, None

    @classmethod
    def process_webhook(cls, provider, event_id, payload, headers):
        log = WebhookLog.objects.create(provider=provider, event_id=event_id, payload=payload, headers=headers)

        from apps.providers.adapters import get_adapter
        adapter = get_adapter(provider)
        if not adapter:
            log.error_message = "adapter_not_found"
            log.save(update_fields=["error_message"])
            return

        # Replay protection
        if event_id:
            from django.core.cache import cache
            replay_key = f"wh_replay:{provider}:{event_id}"
            if cache.get(replay_key):
                log.processed = True
                log.error_message = "duplicate_ignored"
                log.save(update_fields=["processed", "error_message"])
                return
            cache.set(replay_key, True, timeout=259200)  # 72h

        try:
            normalized = adapter.normalize_webhook(payload)
            provider_tx_id = normalized.get("provider_tx_id")
            new_status = normalized.get("status")
            raw_status = normalized.get("raw_status")

            tx = Transaction.objects.filter(provider=provider, provider_tx_id=provider_tx_id).first()
            if not tx:
                tx = Transaction.objects.filter(provider=provider, idempotency_key=normalized.get("idempotency_key")).first()

            if not tx:
                log.error_message = f"transaction_not_found: {provider_tx_id}"
                log.save(update_fields=["error_message"])
                return

            log.transaction = tx
            log.processed = True
            log.save(update_fields=["transaction", "processed"])

            if tx.is_terminal():
                return

            tx.provider_raw_status = raw_status
            if normalized.get("failure_reason"):
                tx.failure_reason = normalized["failure_reason"]
            tx.save(update_fields=["provider_raw_status", "failure_reason", "updated_at"])

            if new_status and tx.can_transition_to(new_status):
                tx.transition_to(new_status, trigger="webhook")
                # TODO: emit RabbitMQ event payment.confirmed / payment.failed

        except Exception as e:
            log.error_message = str(e)[:500]
            log.save(update_fields=["error_message"])
            logger.error(f"Webhook processing error: {e}")

    @classmethod
    def expire_pending(cls):
        now = timezone.now()
        expired = Transaction.objects.filter(status=TransactionStatus.PENDING, expires_at__lt=now)
        count = 0
        for tx in expired:
            try:
                tx.transition_to(TransactionStatus.EXPIRED, trigger="cron_expiry")
                count += 1
            except ValueError:
                pass
        return count

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\urls.py =====
`
from django.urls import path
from apps.payments.views import (
    HealthCheckView, PaymentInitiateView, PaymentDetailView, PaymentListView, PaymentCancelView,
    WebhookOrangeView, WebhookMTNView, WebhookStripeView, WebhookPayPalView,
    ProviderConfigListCreateView, PlatformProviderConfigView,
    AdminStatsView, AdminForceStatusView,
)

urlpatterns = [
    path("payments/health", HealthCheckView.as_view()),
    path("payments/initiate", PaymentInitiateView.as_view()),
    path("payments", PaymentListView.as_view()),
    path("payments/<uuid:transaction_id>", PaymentDetailView.as_view()),
    path("payments/<uuid:transaction_id>/cancel", PaymentCancelView.as_view()),

    # Webhooks (no auth)
    path("payments/webhooks/orange-money", WebhookOrangeView.as_view()),
    path("payments/webhooks/mtn-momo", WebhookMTNView.as_view()),
    path("payments/webhooks/stripe", WebhookStripeView.as_view()),
    path("payments/webhooks/paypal", WebhookPayPalView.as_view()),

    # Providers config
    path("payments/providers", ProviderConfigListCreateView.as_view()),
    path("payments/platforms/<str:platform_id>/providers", PlatformProviderConfigView.as_view()),

    # Admin
    path("payments/admin/stats", AdminStatsView.as_view()),
    path("payments/admin/<uuid:transaction_id>/force-status", AdminForceStatusView.as_view()),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\views.py =====
`
"""AGT Payment Service v1.0 - Views."""
import logging
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.payments.models import Transaction, TransactionStatus, TransactionStatusHistory, ProviderConfig, PlatformPaymentConfig, WebhookLog
from apps.payments.service import PaymentService

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
            cache.set("health", "ok", 5)
            redis_ok = cache.get("health") == "ok"
        except Exception:
            redis_ok = False
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "version": "1.0.0"}, status=code)


class PaymentInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Initier un paiement")
    def post(self, request):
        d = request.data
        required = ["platform_id", "provider", "amount", "currency", "source", "idempotency_key"]
        if not all(d.get(f) for f in required):
            return Response({"detail": f"Champs requis: {', '.join(required)}"}, status=status.HTTP_400_BAD_REQUEST)

        tx, err = PaymentService.initiate(
            platform_id=d["platform_id"], user_id=d.get("user_id"),
            provider=d["provider"], amount=d["amount"], currency=d["currency"],
            source=d["source"], source_reference_id=d.get("source_reference_id"),
            idempotency_key=d["idempotency_key"], phone_number=d.get("phone_number"),
            metadata=d.get("metadata"),
        )

        resp_data = {
            "transaction_id": str(tx.id), "status": tx.status, "provider": tx.provider,
            "amount": float(tx.amount), "currency": tx.currency,
        }
        if tx.payment_url:
            resp_data["payment_url"] = tx.payment_url

        if err == "idempotent_hit":
            resp_data["message"] = "Idempotent request, returning existing transaction"
            return Response(resp_data, status=status.HTTP_200_OK)
        elif err:
            resp_data["message"] = err
            return Response(resp_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        resp_data["message"] = "Payment initiated"
        return Response(resp_data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Detail transaction avec historique statuts")
    def get(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)

        history = TransactionStatusHistory.objects.filter(transaction=tx)
        return Response({
            "id": str(tx.id), "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "provider": tx.provider, "amount": float(tx.amount), "currency": tx.currency,
            "status": tx.status, "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "provider_tx_id": tx.provider_tx_id, "payment_url": tx.payment_url,
            "failure_reason": tx.failure_reason,
            "confirmed_at": tx.confirmed_at.isoformat() if tx.confirmed_at else None,
            "created_at": tx.created_at.isoformat(),
            "status_history": [{"from": h.from_status, "to": h.to_status, "trigger": h.trigger, "at": h.created_at.isoformat()} for h in history],
        })


class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Lister transactions")
    def get(self, request):
        qs = Transaction.objects.all()
        for f in ["platform_id", "user_id", "status", "provider", "source"]:
            v = request.GET.get(f)
            if v:
                qs = qs.filter(**{f: v})
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(t.id), "provider": t.provider, "amount": float(t.amount),
                 "currency": t.currency, "status": t.status, "source": t.source,
                 "created_at": t.created_at.isoformat()} for t in page]
        return paginator.get_paginated_response(data)


class PaymentCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Annuler un paiement pending")
    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if tx.status != TransactionStatus.PENDING:
            return Response({"detail": "Seuls les paiements pending peuvent etre annules."}, status=status.HTTP_400_BAD_REQUEST)
        tx.transition_to(TransactionStatus.CANCELLED, trigger="api_cancel")
        return Response({"transaction_id": str(tx.id), "status": "cancelled", "message": "Payment cancelled"})


# --- Webhooks ---

class WebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def _process(self, request, provider):
        try:
            payload = request.data if isinstance(request.data, dict) else {}
            event_id = payload.get("event_id") or payload.get("id") or request.headers.get("X-Event-Id")
            PaymentService.process_webhook(provider, event_id, payload, dict(request.headers))
        except Exception as e:
            logger.error(f"Webhook {provider} error: {e}")
        return Response({"received": True}, status=status.HTTP_200_OK)


class WebhookOrangeView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback Orange Money")
    def post(self, request):
        return self._process(request, "orange_money")


class WebhookMTNView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback MTN MoMo")
    def post(self, request):
        return self._process(request, "mtn_momo")


class WebhookStripeView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback Stripe")
    def post(self, request):
        return self._process(request, "stripe")


class WebhookPayPalView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback PayPal")
    def post(self, request):
        return self._process(request, "paypal")


# --- Provider Config ---

class ProviderConfigListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Providers"], summary="Creer un provider")
    def post(self, request):
        d = request.data
        if ProviderConfig.objects.filter(provider=d.get("provider")).exists():
            return Response({"detail": "Provider existe deja."}, status=status.HTTP_409_CONFLICT)
        pc = ProviderConfig.objects.create(
            provider=d["provider"], display_name=d.get("display_name", d["provider"]),
            api_base_url=d.get("api_base_url"), supported_currencies=d.get("supported_currencies", []),
        )
        return Response({"id": str(pc.id), "provider": pc.provider, "message": "Provider created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Providers"], summary="Lister les providers")
    def get(self, request):
        providers = ProviderConfig.objects.filter(is_active=True)
        data = [{"provider": p.provider, "display_name": p.display_name, "supported_currencies": p.supported_currencies} for p in providers]
        return Response({"data": data})


class PlatformProviderConfigView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Providers"], summary="Config providers plateforme")
    def get(self, request, platform_id):
        config = PlatformPaymentConfig.get_for_platform(str(platform_id))
        return Response({"platform_id": str(platform_id), "providers_priority": config.providers_priority, "default_currency": config.default_currency})

    @extend_schema(tags=["Providers"], summary="Modifier config providers plateforme")
    def put(self, request, platform_id):
        config, _ = PlatformPaymentConfig.objects.get_or_create(platform_id=platform_id, defaults={"providers_priority": ["orange_money"]})
        if "providers_priority" in request.data:
            config.providers_priority = request.data["providers_priority"]
        if "default_currency" in request.data:
            config.default_currency = request.data["default_currency"]
        config.save()
        return Response({"message": "Config updated"})


# --- Admin ---

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Admin"], summary="Statistiques paiements")
    def get(self, request):
        total = Transaction.objects.count()
        total_amount = Transaction.objects.filter(status="succeeded").aggregate(s=Sum("amount"))["s"] or 0
        succeeded = Transaction.objects.filter(status="succeeded").count()
        success_rate = round((succeeded / total * 100), 1) if total > 0 else 0
        by_provider = list(Transaction.objects.values("provider").annotate(count=Count("id")))
        return Response({
            "total_transactions": total, "total_amount": float(total_amount),
            "success_rate": success_rate, "by_provider": by_provider,
        })


class AdminForceStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Admin"], summary="Forcer statut (verification manuelle)")
    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get("status")
        if new_status not in ["succeeded", "failed"]:
            return Response({"detail": "status doit etre 'succeeded' ou 'failed'."}, status=status.HTTP_400_BAD_REQUEST)
        if tx.is_terminal():
            return Response({"detail": "Transaction deja terminale."}, status=status.HTTP_409_CONFLICT)
        tx.transition_to(new_status, trigger="admin_manual", metadata={"admin_note": request.data.get("note", "")})
        return Response({"transaction_id": str(tx.id), "status": tx.status, "message": "Status forced"})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\tests\test_all.py =====
`
"""AGT Payment Service v1.0 - Tests."""
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from apps.payments.models import Transaction, TransactionStatus, TransactionStatusHistory, VALID_TRANSITIONS
from apps.payments.service import PaymentService


class TestTransactionModel(TestCase):
    def _make_tx(self, **kwargs):
        defaults = {"platform_id": uuid.uuid4(), "provider": "orange_money", "idempotency_key": uuid.uuid4(),
                     "amount": 15000, "currency": "XAF", "source": "subscription"}
        defaults.update(kwargs)
        return Transaction.objects.create(**defaults)

    def test_create(self):
        tx = self._make_tx()
        self.assertEqual(tx.status, "pending")

    def test_valid_transition(self):
        tx = self._make_tx()
        self.assertTrue(tx.can_transition_to("succeeded"))
        self.assertTrue(tx.can_transition_to("failed"))
        self.assertFalse(tx.can_transition_to("cancelled"))  # wait, pending->cancelled is valid
        # Actually pending->cancelled IS valid per our model
        self.assertTrue(tx.can_transition_to("cancelled"))

    def test_transition_creates_history(self):
        tx = self._make_tx()
        tx.transition_to("succeeded", trigger="webhook")
        self.assertEqual(tx.status, "succeeded")
        self.assertIsNotNone(tx.confirmed_at)
        self.assertEqual(TransactionStatusHistory.objects.filter(transaction=tx).count(), 1)

    def test_terminal_no_transition(self):
        tx = self._make_tx()
        tx.transition_to("succeeded", trigger="test")
        self.assertTrue(tx.is_terminal())
        self.assertFalse(tx.can_transition_to("failed"))

    def test_idempotency_unique(self):
        key = uuid.uuid4()
        self._make_tx(idempotency_key=key)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            self._make_tx(idempotency_key=key)


class TestPaymentService(TestCase):
    def test_initiate(self):
        tx, err = PaymentService.initiate(
            platform_id=uuid.uuid4(), user_id=uuid.uuid4(), provider="orange_money",
            amount=15000, currency="XAF", source="subscription",
            source_reference_id=uuid.uuid4(), idempotency_key=uuid.uuid4(),
            phone_number="+237600000000",
        )
        self.assertIsNone(err)
        self.assertEqual(tx.status, "pending")
        self.assertIsNotNone(tx.provider_tx_id)

    def test_idempotent_hit(self):
        key = uuid.uuid4()
        PaymentService.initiate(platform_id=uuid.uuid4(), user_id=None, provider="stripe",
                                 amount=5000, currency="EUR", source="platform_direct",
                                 source_reference_id=None, idempotency_key=key)
        tx2, err = PaymentService.initiate(platform_id=uuid.uuid4(), user_id=None, provider="stripe",
                                            amount=5000, currency="EUR", source="platform_direct",
                                            source_reference_id=None, idempotency_key=key)
        self.assertEqual(err, "idempotent_hit")

    def test_expire_pending(self):
        from django.utils import timezone
        from datetime import timedelta
        tx = Transaction.objects.create(platform_id=uuid.uuid4(), provider="orange_money",
                                         idempotency_key=uuid.uuid4(), amount=1000, currency="XAF",
                                         source="subscription", expires_at=timezone.now() - timedelta(minutes=10))
        count = PaymentService.expire_pending()
        self.assertEqual(count, 1)
        tx.refresh_from_db()
        self.assertEqual(tx.status, "expired")


class TestHealthEndpoint(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/payments/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestPaymentEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    def test_initiate_payment(self):
        resp = self.client.post("/api/v1/payments/initiate", data={
            "platform_id": str(uuid.uuid4()), "provider": "orange_money",
            "amount": 15000, "currency": "XAF", "source": "subscription",
            "idempotency_key": str(uuid.uuid4()), "phone_number": "+237600000000",
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("transaction_id", resp.json())

    def test_list_payments(self):
        resp = self.client.get("/api/v1/payments")
        self.assertEqual(resp.status_code, 200)

    def test_webhook_orange(self):
        # Webhooks are AllowAny
        client = APIClient()
        resp = client.post("/api/v1/payments/webhooks/orange-money", data={
            "txnid": "OM-test", "status": "SUCCESS",
        }, format="json")
        self.assertEqual(resp.status_code, 200)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\payments\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\providers\adapters.py =====
`
"""AGT Payment Service v1.0 - Provider adapters (Strategy pattern)."""
import logging
import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseAdapter:
    name = "base"

    def initiate_payment(self, transaction):
        raise NotImplementedError

    def normalize_webhook(self, payload):
        raise NotImplementedError


class OrangeMoneyAdapter(BaseAdapter):
    name = "orange_money"

    def initiate_payment(self, tx):
        logger.info(f"[ORANGE] USSD push to {tx.phone_number} for {tx.amount} {tx.currency}")
        # En production: appel API Orange Money
        return {"provider_tx_id": f"OM-{tx.id.hex[:8]}"}

    def normalize_webhook(self, payload):
        status_map = {"SUCCESS": "succeeded", "FAILED": "failed", "EXPIRED": "expired", "INITIATED": "pending", "PENDING": "processing"}
        raw = payload.get("status", "")
        return {
            "provider_tx_id": payload.get("txnid") or payload.get("transaction_id"),
            "status": status_map.get(raw, "pending"),
            "raw_status": raw,
            "failure_reason": payload.get("error_message"),
        }


class MTNMoMoAdapter(BaseAdapter):
    name = "mtn_momo"

    def initiate_payment(self, tx):
        logger.info(f"[MTN] USSD push to {tx.phone_number} for {tx.amount} {tx.currency}")
        return {"provider_tx_id": f"MTN-{tx.id.hex[:8]}"}

    def normalize_webhook(self, payload):
        status_map = {"SUCCESSFUL": "succeeded", "FAILED": "failed", "EXPIRED": "expired", "PENDING": "processing"}
        raw = payload.get("status", "")
        return {
            "provider_tx_id": payload.get("externalId") or payload.get("referenceId"),
            "status": status_map.get(raw, "pending"),
            "raw_status": raw,
            "failure_reason": payload.get("reason"),
        }


class StripeAdapter(BaseAdapter):
    name = "stripe"

    def initiate_payment(self, tx):
        logger.info(f"[STRIPE] Creating checkout session for {tx.amount} {tx.currency}")
        # En production: appel Stripe API
        return {
            "provider_tx_id": f"cs_{tx.id.hex[:12]}",
            "payment_url": f"https://checkout.stripe.com/pay/cs_{tx.id.hex[:12]}",
        }

    def normalize_webhook(self, payload):
        event_type = payload.get("type", "")
        status_map = {
            "payment_intent.succeeded": "succeeded",
            "payment_intent.payment_failed": "failed",
            "payment_intent.canceled": "cancelled",
            "payment_intent.created": "pending",
            "payment_intent.processing": "processing",
        }
        obj = payload.get("data", {}).get("object", {})
        return {
            "provider_tx_id": obj.get("id"),
            "status": status_map.get(event_type, "pending"),
            "raw_status": event_type,
            "failure_reason": obj.get("last_payment_error", {}).get("message") if isinstance(obj.get("last_payment_error"), dict) else None,
        }


class PayPalAdapter(BaseAdapter):
    name = "paypal"

    def initiate_payment(self, tx):
        logger.info(f"[PAYPAL] Creating order for {tx.amount} {tx.currency}")
        return {
            "provider_tx_id": f"PP-{tx.id.hex[:8]}",
            "payment_url": f"https://www.paypal.com/checkoutnow?token=PP-{tx.id.hex[:8]}",
        }

    def normalize_webhook(self, payload):
        event_type = payload.get("event_type", "")
        status_map = {"PAYMENT.CAPTURE.COMPLETED": "succeeded", "PAYMENT.CAPTURE.DENIED": "failed", "CHECKOUT.ORDER.APPROVED": "processing"}
        resource = payload.get("resource", {})
        return {
            "provider_tx_id": resource.get("id"),
            "status": status_map.get(event_type, "pending"),
            "raw_status": event_type,
        }


ADAPTERS = {
    "orange_money": OrangeMoneyAdapter(),
    "mtn_momo": MTNMoMoAdapter(),
    "stripe": StripeAdapter(),
    "paypal": PayPalAdapter(),
}


def get_adapter(provider):
    return ADAPTERS.get(provider)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\providers\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\apps\webhooks\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\common\authentication.py =====
`
import jwt, logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.platform_id = p.get("platform_id")
        self.is_authenticated = True

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return None
        token = h.split(" ", 1)[1]
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached:
            return JWTPayload(cached), cached
        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try:
            payload = jwt.decode(token, pk, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload
    def authenticate_header(self, request):
        return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\settings.py =====
`
from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.staticfiles", "rest_framework", "drf_spectacular", "corsheaders", "apps.payments", "apps.providers", "apps.webhooks"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]
import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/5")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL, "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
def _read_key(path):
    try:
        with open(path, "r") as f: return f.read()
    except FileNotFoundError: return ""
AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ["common.authentication.JWTAuthentication"], "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"], "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"], "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", "UNAUTHENTICATED_USER": None}
SPECTACULAR_SETTINGS = {"TITLE": "AGT Payment Service API", "VERSION": "1.0.0", "DESCRIPTION": "Paiements multi-provider: Orange Money, MTN MoMo, Stripe, PayPal.", "TAGS": [{"name": "Health"}, {"name": "Payments"}, {"name": "Webhooks"}, {"name": "Providers"}, {"name": "Admin"}]}
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {"version": 1, "disable_existing_loggers": False, "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\settings_test.py =====
`
from config.settings import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
LOGGING = {"version": 1, "disable_existing_loggers": True, "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path("api/v1/", include("apps.payments.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-payment\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\.env =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://search_user:search_password@db:5432/agt_search_db
REDIS_URL=redis://redis:6379/7
ELASTICSEARCH_URL=http://elasticsearch:9200
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\.env.example =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://search_user:search_password@db:5432/agt_search_db
REDIS_URL=redis://redis:6379/7
ELASTICSEARCH_URL=http://elasticsearch:9200
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\CDC_v1.0.md =====
`
# AGT Search Service - CDC v1.0

> Recherche full-text Elasticsearch, indexation dynamique, autocomplete, historique.

## Tables (6)
indexes_registry, index_schemas, search_configs, synonyms, search_history, popular_searches

## Elasticsearch
Index par plateforme ({platform_id}_{index_name}). Full-text, fuzzy, facettes, boost, autocomplete.

## Endpoints principaux
- CRUD indexes avec schema dynamique
- Indexation documents (unitaire + bulk 500 max)
- POST /search/query (full-text + filtres + facettes)
- GET /search/autocomplete (< 50ms)
- GET/DELETE /search/history (RGPD)
- GET /search/popular
- GET/PUT config + synonymes par index

## Port : 7007 | Elasticsearch : 9200

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_search_db
    environment:
      POSTGRES_DB: agt_search_db
      POSTGRES_USER: search_user
      POSTGRES_PASSWORD: search_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5438:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U search_user -d agt_search_db"]
      interval: 10s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    container_name: agt_search_redis
    volumes:
      - redis_data:/data
    ports:
      - "6385:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.0
    container_name: agt_search_es
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 5
  search:
    build:
      context: .
      target: production
    container_name: agt_search_service
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://search_user:search_password@db:5432/agt_search_db
      REDIS_URL: redis://redis:6379/7
      ELASTICSEARCH_URL: http://elasticsearch:9200
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7007:7007"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7007/api/v1/search/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  search-dev:
    build:
      context: .
      target: builder
    container_name: agt_search_dev
    command: sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:7007"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://search_user:search_password@db:5432/agt_search_db
      REDIS_URL: redis://redis:6379/7
      ELASTICSEARCH_URL: http://elasticsearch:9200
      DEBUG: "True"
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7007:7007"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    profiles:
      - dev
volumes:
  postgres_data:
  redis_data:
  es_data:

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7007
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7007", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\manage.py =====
`
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == "__main__": main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\README.md =====
`
# AGT Search Service - v1.0

Recherche full-text Elasticsearch, indexation dynamique, autocomplete, historique.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
# Ouvrir Docker Desktop
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

> Elasticsearch prend ~30s au premier demarrage.

## Documentation API
| URL | Description |
|-----|-------------|
| http://localhost:7007/api/v1/docs/ | Swagger UI |
| http://localhost:7007/api/v1/redoc/ | ReDoc |
| http://localhost:9200 | Elasticsearch |

## Tests
```bash
docker compose exec search python -m pytest -v
```

## Endpoints
- CRUD /search/indexes (+ schema)
- POST/DELETE /search/indexes/{name}/documents
- POST /search/indexes/{name}/documents/bulk
- POST /search/query (full-text + filtres + facettes)
- GET /search/autocomplete?index=...&prefix=...
- GET/DELETE /search/history
- GET /search/popular?index=...
- GET/PUT /search/indexes/{name}/config
- PUT/GET /search/indexes/{name}/synonyms
- GET /search/stats

Port : **7007**

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\requirements.txt =====
`
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.4
elasticsearch==8.13.0
PyJWT==2.8.0
cryptography==42.0.5
drf-spectacular==0.27.2
python-decouple==3.8
gunicorn==22.0.0
pytest==8.2.0
pytest-django==4.8.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\indexes\models.py =====
`
"""AGT Search Service v1.0 - Modeles PostgreSQL (metadata, configs, historique)."""
import uuid
from django.db import models


class IndexRegistry(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("rebuilding", "Rebuilding"), ("deleted", "Deleted")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    platform_id = models.UUIDField(db_index=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    document_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "indexes_registry"
        unique_together = [("name", "platform_id")]
        ordering = ["name"]


class IndexSchema(models.Model):
    FIELD_TYPES = [("text", "Text"), ("keyword", "Keyword"), ("number", "Number"), ("date", "Date"), ("boolean", "Boolean")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.ForeignKey(IndexRegistry, on_delete=models.CASCADE, related_name="schema_fields")
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    searchable = models.BooleanField(default=True)
    filterable = models.BooleanField(default=False)
    sortable = models.BooleanField(default=False)
    autocomplete = models.BooleanField(default=False)
    boost_weight = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "index_schemas"
        unique_together = [("index", "field_name")]


class SearchConfig(models.Model):
    index = models.OneToOneField(IndexRegistry, on_delete=models.CASCADE, primary_key=True, related_name="config")
    analyzer = models.CharField(max_length=50, default="french")
    fuzzy_enabled = models.BooleanField(default=True)
    fuzzy_distance = models.IntegerField(default=1)
    highlight_enabled = models.BooleanField(default=True)
    min_score = models.FloatField(null=True, blank=True)
    max_results = models.IntegerField(default=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_configs"


class Synonym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.ForeignKey(IndexRegistry, on_delete=models.CASCADE, related_name="synonyms")
    term = models.CharField(max_length=100)
    equivalents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "synonyms"


class SearchHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    platform_id = models.UUIDField()
    index_name = models.CharField(max_length=100)
    query = models.TextField()
    filters_applied = models.JSONField(null=True, blank=True)
    result_count = models.IntegerField()
    took_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "search_history"
        ordering = ["-created_at"]


class PopularSearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index_name = models.CharField(max_length=100)
    platform_id = models.UUIDField()
    term = models.CharField(max_length=255)
    search_count = models.BigIntegerField(default=0)
    last_searched_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "popular_searches"
        unique_together = [("index_name", "platform_id", "term")]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\indexes\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\es_service.py =====
`
"""AGT Search Service v1.0 - Elasticsearch client service."""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_es():
    try:
        from elasticsearch import Elasticsearch
        return Elasticsearch(getattr(settings, "ELASTICSEARCH_URL", "http://localhost:9200"))
    except Exception as e:
        logger.error(f"ES connection failed: {e}")
        return None


class ESService:

    @classmethod
    def create_index(cls, index_name, schema_fields):
        es = _get_es()
        if not es:
            return False
        properties = {}
        for f in schema_fields:
            ft = f["field_type"]
            if ft == "text":
                mapping = {"type": "text"}
                if f.get("autocomplete"):
                    mapping["fields"] = {"autocomplete": {"type": "text", "analyzer": "autocomplete_analyzer"}}
            elif ft == "keyword":
                mapping = {"type": "keyword"}
            elif ft == "number":
                mapping = {"type": "float"}
            elif ft == "date":
                mapping = {"type": "date"}
            elif ft == "boolean":
                mapping = {"type": "boolean"}
            else:
                mapping = {"type": "text"}
            properties[f["field_name"]] = mapping

        body = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "autocomplete_analyzer": {
                            "type": "custom", "tokenizer": "standard",
                            "filter": ["lowercase", "autocomplete_filter"]
                        }
                    },
                    "filter": {
                        "autocomplete_filter": {"type": "edge_ngram", "min_gram": 2, "max_gram": 20}
                    }
                }
            },
            "mappings": {"properties": properties}
        }
        try:
            es.indices.create(index=index_name, body=body, ignore=400)
            return True
        except Exception as e:
            logger.error(f"ES create index failed: {e}")
            return False

    @classmethod
    def index_document(cls, index_name, doc_id, data):
        es = _get_es()
        if not es:
            return False
        try:
            es.index(index=index_name, id=doc_id, body=data)
            return True
        except Exception as e:
            logger.error(f"ES index doc failed: {e}")
            return False

    @classmethod
    def delete_document(cls, index_name, doc_id):
        es = _get_es()
        if not es:
            return False
        try:
            es.delete(index=index_name, id=doc_id, ignore=404)
            return True
        except Exception as e:
            logger.error(f"ES delete doc failed: {e}")
            return False

    @classmethod
    def search(cls, index_name, query, filters=None, sort=None, page=1, limit=20, fuzzy=True, highlight=True):
        es = _get_es()
        if not es:
            return {"results": [], "total": 0, "took_ms": 0}

        body = {"query": {"bool": {"must": [], "filter": []}}}
        if query:
            match = {"multi_match": {"query": query, "fields": ["*"], "type": "best_fields"}}
            if fuzzy:
                match["multi_match"]["fuzziness"] = "AUTO"
            body["query"]["bool"]["must"].append(match)

        for f in (filters or []):
            op = f.get("operator", "eq")
            if op == "eq":
                body["query"]["bool"]["filter"].append({"term": {f["field"]: f["value"]}})
            elif op == "range":
                r = {}
                if "min" in f:
                    r["gte"] = f["min"]
                if "max" in f:
                    r["lte"] = f["max"]
                body["query"]["bool"]["filter"].append({"range": {f["field"]: r}})

        if sort:
            body["sort"] = [{sort["field"]: {"order": sort.get("order", "desc")}}]

        if highlight:
            body["highlight"] = {"fields": {"*": {}}}

        body["from"] = (page - 1) * limit
        body["size"] = limit

        try:
            resp = es.search(index=index_name, body=body)
            hits = resp.get("hits", {})
            results = []
            for h in hits.get("hits", []):
                r = {"doc_id": h["_id"], "score": h.get("_score"), "data": h.get("_source", {})}
                if "highlight" in h:
                    r["highlights"] = h["highlight"]
                results.append(r)
            return {"results": results, "total": hits.get("total", {}).get("value", 0),
                    "took_ms": resp.get("took", 0), "page": page, "limit": limit}
        except Exception as e:
            logger.error(f"ES search failed: {e}")
            return {"results": [], "total": 0, "took_ms": 0}

    @classmethod
    def autocomplete(cls, index_name, prefix, limit=8):
        es = _get_es()
        if not es:
            return []
        try:
            body = {"query": {"multi_match": {"query": prefix, "type": "phrase_prefix", "fields": ["*"]}}, "size": limit}
            resp = es.search(index=index_name, body=body)
            return [{"text": h["_source"].get("title") or h["_source"].get("name") or list(h["_source"].values())[0],
                     "doc_id": h["_id"]} for h in resp.get("hits", {}).get("hits", [])]
        except Exception as e:
            logger.error(f"ES autocomplete failed: {e}")
            return []

    @classmethod
    def bulk_operations(cls, index_name, operations):
        es = _get_es()
        if not es:
            return {"succeeded": 0, "failed": len(operations), "errors": []}
        succeeded = failed = 0
        errors = []
        for op in operations:
            try:
                if op["action"] == "index":
                    es.index(index=index_name, id=op["doc_id"], body=op.get("data", {}))
                    succeeded += 1
                elif op["action"] == "delete":
                    es.delete(index=index_name, id=op["doc_id"], ignore=404)
                    succeeded += 1
            except Exception as e:
                failed += 1
                errors.append({"doc_id": op.get("doc_id"), "error": str(e)[:200]})
        return {"total": len(operations), "succeeded": succeeded, "failed": failed, "errors": errors}

    @classmethod
    def delete_index(cls, index_name):
        es = _get_es()
        if not es:
            return False
        try:
            es.indices.delete(index=index_name, ignore=404)
            return True
        except Exception as e:
            logger.error(f"ES delete index failed: {e}")
            return False

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\urls.py =====
`
from django.urls import path
from apps.search.views import (
    HealthCheckView, IndexListCreateView, IndexDetailView,
    DocumentIndexView, DocumentDeleteView, DocumentBulkView,
    SearchQueryView, AutocompleteView,
    HistoryView, HistoryPurgeView, PopularView,
    ConfigView, SynonymsView, StatsView,
)
urlpatterns = [
    path("search/health", HealthCheckView.as_view()),
    path("search/indexes", IndexListCreateView.as_view()),
    path("search/indexes/<str:index_name>", IndexDetailView.as_view()),
    path("search/indexes/<str:index_name>/documents", DocumentIndexView.as_view()),
    path("search/indexes/<str:index_name>/documents/<str:doc_id>", DocumentDeleteView.as_view()),
    path("search/indexes/<str:index_name>/documents/bulk", DocumentBulkView.as_view()),
    path("search/indexes/<str:index_name>/config", ConfigView.as_view()),
    path("search/indexes/<str:index_name>/synonyms", SynonymsView.as_view()),
    path("search/query", SearchQueryView.as_view()),
    path("search/autocomplete", AutocompleteView.as_view()),
    path("search/history", HistoryView.as_view()),
    path("search/history/by-user/<uuid:user_id>", HistoryPurgeView.as_view()),
    path("search/popular", PopularView.as_view()),
    path("search/stats", StatsView.as_view()),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\views.py =====
`
"""AGT Search Service v1.0 - Views."""
import logging, time
from django.db.models import Count, Avg, Sum, F
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.indexes.models import IndexRegistry, IndexSchema, SearchConfig, Synonym, SearchHistory, PopularSearch
from apps.search.es_service import ESService

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
        db_ok = redis_ok = es_ok = True
        try:
            from django.db import connection; connection.ensure_connection()
        except Exception: db_ok = False
        try:
            from django.core.cache import cache; cache.set("h", "ok", 5); redis_ok = cache.get("h") == "ok"
        except Exception: redis_ok = False
        try:
            from apps.search.es_service import _get_es
            es = _get_es()
            es_ok = es.ping() if es else False
        except Exception: es_ok = False
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok and es_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "elasticsearch": "ok" if es_ok else "error", "version": "1.0.0"}, status=code)


# --- Indexes CRUD ---

class IndexListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Indexes"], summary="Creer un index")
    def post(self, request):
        d = request.data
        name, pid = d.get("name"), d.get("platform_id")
        if not name or not pid:
            return Response({"detail": "name et platform_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        if IndexRegistry.objects.filter(name=name, platform_id=pid).exists():
            return Response({"detail": "Index existe deja."}, status=status.HTTP_409_CONFLICT)
        idx = IndexRegistry.objects.create(name=name, platform_id=pid, description=d.get("description"))
        schema = d.get("schema", [])
        for f in schema:
            IndexSchema.objects.create(index=idx, field_name=f["field_name"], field_type=f.get("field_type", "text"),
                                        searchable=f.get("searchable", True), filterable=f.get("filterable", False),
                                        sortable=f.get("sortable", False), autocomplete=f.get("autocomplete", False),
                                        boost_weight=f.get("boost_weight", 1))
        SearchConfig.objects.create(index=idx)
        es_name = f"{pid}_{name}"
        ESService.create_index(es_name, schema)
        return Response({"id": str(idx.id), "name": name, "es_index": es_name, "message": "Index created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Indexes"], summary="Lister les index")
    def get(self, request):
        qs = IndexRegistry.objects.filter(status="active")
        pid = request.GET.get("platform_id")
        if pid:
            qs = qs.filter(platform_id=pid)
        data = [{"id": str(i.id), "name": i.name, "platform_id": str(i.platform_id),
                 "document_count": i.document_count, "status": i.status} for i in qs]
        return Response({"data": data})


class IndexDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Indexes"], summary="Detail index avec schema")
    def get(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        fields = [{"field_name": f.field_name, "field_type": f.field_type, "searchable": f.searchable,
                    "filterable": f.filterable, "autocomplete": f.autocomplete} for f in idx.schema_fields.all()]
        return Response({"id": str(idx.id), "name": idx.name, "platform_id": str(idx.platform_id),
                         "document_count": idx.document_count, "schema": fields})

    @extend_schema(tags=["Indexes"], summary="Supprimer un index")
    def delete(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ESService.delete_index(f"{idx.platform_id}_{index_name}")
        idx.status = "deleted"
        idx.save(update_fields=["status", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Documents ---

class DocumentIndexView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Documents"], summary="Indexer un document")
    def post(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        doc_id = request.data.get("doc_id")
        data = request.data.get("data", {})
        if not doc_id:
            return Response({"detail": "doc_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        es_name = f"{idx.platform_id}_{index_name}"
        ESService.index_document(es_name, doc_id, data)
        idx.document_count = F("document_count") + 1
        idx.save(update_fields=["document_count", "updated_at"])
        return Response({"doc_id": doc_id, "index": index_name, "message": "Document indexed"}, status=status.HTTP_201_CREATED)


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Documents"], summary="Supprimer un document")
    def delete(self, request, index_name, doc_id):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ESService.delete_document(f"{idx.platform_id}_{index_name}", doc_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentBulkView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Documents"], summary="Indexation en masse")
    def post(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ops = request.data.get("operations", [])
        if len(ops) > 500:
            return Response({"detail": "Max 500 operations."}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        result = ESService.bulk_operations(f"{idx.platform_id}_{index_name}", ops)
        return Response(result, status=status.HTTP_207_MULTI_STATUS)


# --- Search ---

class SearchQueryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Search"], summary="Recherche full-text")
    def post(self, request):
        d = request.data
        index_name = d.get("index")
        query = d.get("query", "")
        if not index_name:
            return Response({"detail": "index requis."}, status=status.HTTP_400_BAD_REQUEST)
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)

        es_name = f"{idx.platform_id}_{index_name}"
        cfg = SearchConfig.objects.filter(index=idx).first()
        result = ESService.search(es_name, query, d.get("filters"), d.get("sort"),
                                   d.get("page", 1), min(d.get("limit", 20), cfg.max_results if cfg else 100),
                                   fuzzy=cfg.fuzzy_enabled if cfg else True,
                                   highlight=cfg.highlight_enabled if cfg else True)

        # Log historique
        uid = getattr(request.user, "auth_user_id", None)
        pid = str(getattr(request.user, "platform_id", idx.platform_id))
        SearchHistory.objects.create(user_id=uid, platform_id=pid, index_name=index_name,
                                      query=query, filters_applied=d.get("filters"),
                                      result_count=result["total"], took_ms=result["took_ms"])

        # Popular search update
        if query.strip():
            ps, _ = PopularSearch.objects.get_or_create(index_name=index_name, platform_id=pid, term=query.strip().lower(),
                                                          defaults={"search_count": 0})
            ps.search_count += 1
            ps.save(update_fields=["search_count", "last_searched_at", "updated_at"])

        return Response(result)


class AutocompleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Search"], summary="Auto-completion (< 50ms)")
    def get(self, request):
        index_name = request.GET.get("index")
        prefix = request.GET.get("prefix", "")
        if not index_name or not prefix:
            return Response({"detail": "index et prefix requis."}, status=status.HTTP_400_BAD_REQUEST)
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        limit = min(int(request.GET.get("limit", 8)), 20)
        suggestions = ESService.autocomplete(f"{idx.platform_id}_{index_name}", prefix, limit)
        return Response({"suggestions": suggestions})


# --- History ---

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["History"], summary="Historique recherches")
    def get(self, request):
        uid = getattr(request.user, "auth_user_id", None)
        qs = SearchHistory.objects.filter(user_id=uid)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"query": h.query, "index": h.index_name, "result_count": h.result_count,
                 "took_ms": h.took_ms, "created_at": h.created_at.isoformat()} for h in page]
        return paginator.get_paginated_response(data)

    @extend_schema(tags=["History"], summary="Supprimer historique (RGPD)")
    def delete(self, request):
        uid = getattr(request.user, "auth_user_id", None)
        deleted, _ = SearchHistory.objects.filter(user_id=uid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryPurgeView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["History"], summary="Purge RGPD par userId (S2S)")
    def delete(self, request, user_id):
        deleted, _ = SearchHistory.objects.filter(user_id=user_id).delete()
        return Response({"message": "Search history purged", "user_id": str(user_id), "entries_deleted": deleted})


class PopularView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["History"], summary="Recherches populaires")
    def get(self, request):
        index_name = request.GET.get("index")
        if not index_name:
            return Response({"detail": "index requis."}, status=status.HTTP_400_BAD_REQUEST)
        limit = int(request.GET.get("limit", 10))
        popular = PopularSearch.objects.filter(index_name=index_name).order_by("-search_count")[:limit]
        return Response({"data": [{"term": p.term, "count": p.search_count} for p in popular]})


# --- Config ---

class ConfigView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Config"], summary="Lire/modifier config index")
    def get(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        cfg = SearchConfig.objects.filter(index=idx).first()
        if not cfg:
            return Response({"detail": "Config introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"analyzer": cfg.analyzer, "fuzzy_enabled": cfg.fuzzy_enabled,
                         "fuzzy_distance": cfg.fuzzy_distance, "highlight_enabled": cfg.highlight_enabled,
                         "min_score": cfg.min_score, "max_results": cfg.max_results})

    def put(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        cfg, _ = SearchConfig.objects.get_or_create(index=idx)
        d = request.data
        for f in ["analyzer", "fuzzy_enabled", "fuzzy_distance", "highlight_enabled", "min_score", "max_results"]:
            if f in d:
                setattr(cfg, f, d[f])
        cfg.save()
        return Response({"message": "Config updated"})


class SynonymsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Config"], summary="Gerer synonymes")
    def put(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        Synonym.objects.filter(index=idx).delete()
        for s in request.data.get("synonyms", []):
            Synonym.objects.create(index=idx, term=s["term"], equivalents=",".join(s.get("equivalents", [])))
        return Response({"message": "Synonyms updated"})

    def get(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        syns = Synonym.objects.filter(index=idx)
        return Response({"data": [{"term": s.term, "equivalents": s.equivalents.split(",")} for s in syns]})


# --- Stats ---

class StatsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Stats"], summary="Statistiques globales")
    def get(self, request):
        total = SearchHistory.objects.count()
        avg_ms = SearchHistory.objects.aggregate(avg=Avg("took_ms"))["avg"] or 0
        return Response({"total_searches": total, "avg_response_ms": round(avg_ms, 1)})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\tests\test_all.py =====
`
"""AGT Search Service v1.0 - Tests (sans ES)."""
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from apps.indexes.models import IndexRegistry, IndexSchema, SearchConfig, SearchHistory, PopularSearch

class TestModels(TestCase):
    def test_create_index(self):
        idx = IndexRegistry.objects.create(name="products", platform_id=uuid.uuid4())
        self.assertEqual(idx.status, "active")
        self.assertEqual(idx.document_count, 0)

    def test_schema(self):
        idx = IndexRegistry.objects.create(name="test", platform_id=uuid.uuid4())
        IndexSchema.objects.create(index=idx, field_name="title", field_type="text", searchable=True)
        self.assertEqual(idx.schema_fields.count(), 1)

    def test_search_history(self):
        SearchHistory.objects.create(user_id=uuid.uuid4(), platform_id=uuid.uuid4(),
                                      index_name="products", query="test", result_count=10, took_ms=50)
        self.assertEqual(SearchHistory.objects.count(), 1)

    def test_popular_search(self):
        ps = PopularSearch.objects.create(index_name="products", platform_id=uuid.uuid4(), term="nike", search_count=42)
        self.assertEqual(ps.search_count, 42)

class TestHealth(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/search/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")

class TestIndexEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())
    def test_list_indexes(self):
        resp = self.client.get("/api/v1/search/indexes")
        self.assertEqual(resp.status_code, 200)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\apps\search\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\common\authentication.py =====
`
import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.platform_id = p.get("platform_id")
        self.is_authenticated = True
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "): return None
        token = h.split(" ", 1)[1]
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached: return JWTPayload(cached), cached
        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk: raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try: payload = jwt.decode(token, pk, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError: raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError: raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload
    def authenticate_header(self, request): return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\settings.py =====
`
from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.staticfiles", "rest_framework", "drf_spectacular", "corsheaders", "apps.indexes", "apps.search"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]
import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/7")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL, "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
ELASTICSEARCH_URL = config("ELASTICSEARCH_URL", default="http://localhost:9200")
def _read_key(path):
    try:
        with open(path, "r") as f: return f.read()
    except FileNotFoundError: return ""
AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ["common.authentication.JWTAuthentication"], "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"], "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"], "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", "UNAUTHENTICATED_USER": None}
SPECTACULAR_SETTINGS = {"TITLE": "AGT Search Service API", "VERSION": "1.0.0", "DESCRIPTION": "Recherche full-text Elasticsearch, indexation, autocomplete, historique.", "TAGS": [{"name": "Health"}, {"name": "Indexes"}, {"name": "Documents"}, {"name": "Search"}, {"name": "History"}, {"name": "Config"}, {"name": "Stats"}]}
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {"version": 1, "disable_existing_loggers": False, "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\settings_test.py =====
`
from config.settings import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
ELASTICSEARCH_URL = "http://localhost:9200"
LOGGING = {"version": 1, "disable_existing_loggers": True, "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path("api/v1/", include("apps.search.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-search\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\.env =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://sub_user:sub_password@db:5432/agt_subscription_db
REDIS_URL=redis://redis:6379/4
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
PAYMENT_SERVICE_URL=http://payment-service:7005/api/v1
NOTIFICATION_SERVICE_URL=http://notification-service:7002/api/v1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\.env.example =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://sub_user:sub_password@db:5432/agt_subscription_db
REDIS_URL=redis://redis:6379/4
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
PAYMENT_SERVICE_URL=http://payment-service:7005/api/v1
NOTIFICATION_SERVICE_URL=http://notification-service:7002/api/v1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\CDC_v1.0.md =====
`
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

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_sub_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: agt_subscription_db
      POSTGRES_USER: sub_user
      POSTGRES_PASSWORD: sub_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5435:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sub_user -d agt_subscription_db"]
      interval: 10s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    container_name: agt_sub_redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    ports:
      - "6382:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  subscription:
    build:
      context: .
      target: production
    container_name: agt_sub_service
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://sub_user:sub_password@db:5432/agt_subscription_db
      REDIS_URL: redis://redis:6379/4
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7004:7004"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7004/api/v1/subscriptions/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  subscription-dev:
    build:
      context: .
      target: builder
    container_name: agt_sub_dev
    restart: unless-stopped
    command: sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:7004"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://sub_user:sub_password@db:5432/agt_subscription_db
      REDIS_URL: redis://redis:6379/4
      DEBUG: "True"
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7004:7004"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles:
      - dev
volumes:
  postgres_data:
  redis_data:

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7004
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7004", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\manage.py =====
`
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == "__main__":
    main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\README.md =====
`
# AGT Subscription Service - v1.0

Plans, abonnements, quotas temps reel, prorata, trial, organisations B2B.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
# Ouvrir Docker Desktop
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Swagger
http://localhost:7004/api/v1/docs/

## Tests
```bash
docker compose exec subscription python -m pytest -v
```

## Endpoints principaux

### Plans
- POST/GET /subscriptions/plans
- GET/PUT /subscriptions/plans/{id}
- POST /subscriptions/plans/{id}/archive

### Subscriptions
- POST /subscriptions (create)
- GET /subscriptions/list
- GET /subscriptions/{id}
- POST /subscriptions/{id}/cancel
- POST /subscriptions/{id}/change-plan (prorata)
- POST /subscriptions/{id}/activate
- POST /subscriptions/{id}/reactivate
- GET /subscriptions/{id}/usage

### Quotas (S2S)
- POST /subscriptions/quotas/check (< 50ms)
- POST /subscriptions/quotas/increment
- POST /subscriptions/quotas/reserve
- POST /subscriptions/quotas/confirm
- POST /subscriptions/quotas/release

### Organizations B2B
- POST/GET /organizations
- POST/GET/DELETE /organizations/{id}/members

### Config
- GET/PUT /subscriptions/config/{platformId}

Voir [CDC_v1.0.md](./CDC_v1.0.md)

Port : **7004**

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\requirements.txt =====
`
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.4
PyJWT==2.8.0
cryptography==42.0.5
drf-spectacular==0.27.2
python-decouple==3.8
httpx==0.27.0
gunicorn==22.0.0
pytest==8.2.0
pytest-django==4.8.0
factory-boy==3.3.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\organizations\models.py =====
`
"""AGT Subscription Service v1.0 - Organizations B2B."""
import uuid
from django.db import models


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=150)
    owner_user_id = models.UUIDField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations"
        unique_together = [("platform_id", "name")]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"


class OrganizationMember(models.Model):
    ROLE_CHOICES = [("owner", "Owner"), ("member", "Member")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    user_id = models.UUIDField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "organization_members"
        unique_together = [("organization", "user_id")]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\organizations\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\plans\models.py =====
`
"""AGT Subscription Service v1.0 - Modeles Plans, Prices, Quotas."""
import uuid
from django.db import models


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    tier_order = models.IntegerField(default=0)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plans"
        unique_together = [("platform_id", "slug")]
        ordering = ["tier_order", "name"]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"

    def has_active_subscriptions(self):
        return self.subscriptions.exclude(status__in=["expired", "cancelled"]).exists()


class PlanPrice(models.Model):
    CYCLE_CHOICES = [("monthly", "Monthly"), ("yearly", "Yearly"), ("custom", "Custom")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="prices")
    billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES)
    cycle_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plan_prices"
        unique_together = [("plan", "billing_cycle", "currency")]

    def get_cycle_days(self):
        if self.billing_cycle == "monthly":
            return 30
        elif self.billing_cycle == "yearly":
            return 365
        return self.cycle_days or 30

    def price_per_day(self):
        return self.price / self.get_cycle_days()


class PlanQuota(models.Model):
    OVERAGE_CHOICES = [("hard", "Hard Limit"), ("overage", "Overage Allowed")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="quotas")
    quota_key = models.CharField(max_length=50)
    limit_value = models.IntegerField()
    is_cyclical = models.BooleanField(default=True)
    overage_policy = models.CharField(max_length=10, choices=OVERAGE_CHOICES, default="hard")
    overage_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plan_quotas"
        unique_together = [("plan", "quota_key")]

    def __str__(self):
        return f"{self.quota_key}: {self.limit_value} ({self.overage_policy})"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\plans\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\quotas\service.py =====
`
"""AGT Subscription Service v1.0 - Quotas service (chemin critique < 50ms)."""
import logging
from django.core.cache import cache
from django.utils import timezone
from apps.subscriptions.models import Subscription, SubscriptionQuotaUsage, QuotaReservation, SubscriptionStatus
from apps.plans.models import PlanQuota

logger = logging.getLogger(__name__)


class QuotaService:
    CACHE_TTL = 30

    @classmethod
    def _cache_key(cls, sub_id, quota_key):
        return f"quota:{sub_id}:{quota_key}"

    @classmethod
    def _get_active_sub(cls, platform_id, subscriber_type, subscriber_id):
        return Subscription.objects.filter(
            platform_id=platform_id, subscriber_type=subscriber_type,
            subscriber_id=subscriber_id, status__in=[
                SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL, SubscriptionStatus.GRACE
            ]
        ).select_related("plan").first()

    @classmethod
    def check(cls, platform_id, subscriber_type, subscriber_id, quota_key, requested=1):
        sub = cls._get_active_sub(platform_id, subscriber_type, subscriber_id)
        if not sub:
            return {"allowed": False, "reason": "no_active_subscription"}

        # Cache Redis
        ck = cls._cache_key(sub.id, quota_key)
        cached = cache.get(ck)
        if cached:
            remaining = cached["limit"] - cached["used"]
            allowed = remaining >= requested if cached["overage_policy"] == "hard" else True
            return {**cached, "remaining": max(0, remaining), "allowed": allowed, "requested": requested}

        plan_quota = PlanQuota.objects.filter(plan=sub.plan, quota_key=quota_key).first()
        if not plan_quota:
            return {"allowed": True, "reason": "quota_not_defined", "quota_key": quota_key}

        usage = SubscriptionQuotaUsage.objects.filter(
            subscription=sub, quota_key=quota_key,
            period_start=sub.current_period_start
        ).first()
        used = usage.used if usage else 0
        overage = usage.overage if usage else 0

        # Compter reservations pending
        reserved = QuotaReservation.objects.filter(
            subscription=sub, quota_key=quota_key, status="pending", expires_at__gt=timezone.now()
        ).count()

        effective_used = used + reserved
        remaining = plan_quota.limit_value - effective_used
        allowed = remaining >= requested if plan_quota.overage_policy == "hard" else True

        result = {
            "allowed": allowed, "quota_key": quota_key,
            "limit": plan_quota.limit_value, "used": effective_used,
            "remaining": max(0, remaining), "overage": overage,
            "overage_policy": plan_quota.overage_policy,
        }
        cache.set(ck, result, timeout=cls.CACHE_TTL)
        return result

    @classmethod
    def increment(cls, platform_id, subscriber_type, subscriber_id, quota_key, amount=1):
        sub = cls._get_active_sub(platform_id, subscriber_type, subscriber_id)
        if not sub:
            return None, "no_active_subscription"

        plan_quota = PlanQuota.objects.filter(plan=sub.plan, quota_key=quota_key).first()
        if not plan_quota:
            return None, "quota_not_defined"

        usage, _ = SubscriptionQuotaUsage.objects.get_or_create(
            subscription=sub, quota_key=quota_key, period_start=sub.current_period_start,
            defaults={"period_end": sub.current_period_end, "used": 0, "overage": 0}
        )

        new_used = usage.used + amount
        if plan_quota.overage_policy == "hard" and new_used > plan_quota.limit_value:
            return None, "hard_limit_exceeded"

        if new_used > plan_quota.limit_value:
            usage.overage += (new_used - plan_quota.limit_value) - usage.overage
            usage.overage = max(0, new_used - plan_quota.limit_value)

        usage.used = new_used
        usage.save(update_fields=["used", "overage", "updated_at"])

        # Invalider cache
        cache.delete(cls._cache_key(sub.id, quota_key))

        return {
            "quota_key": quota_key, "used": usage.used,
            "limit": plan_quota.limit_value, "overage": usage.overage,
        }, None

    @classmethod
    def reserve(cls, platform_id, subscriber_type, subscriber_id, quota_key, amount=1, ttl_seconds=300):
        sub = cls._get_active_sub(platform_id, subscriber_type, subscriber_id)
        if not sub:
            return None, "no_active_subscription"

        check_result = cls.check(platform_id, subscriber_type, subscriber_id, quota_key, amount)
        if not check_result.get("allowed"):
            return None, "quota_exceeded"

        reservation = QuotaReservation.objects.create(
            subscription=sub, quota_key=quota_key, amount=amount,
            expires_at=timezone.now() + timezone.timedelta(seconds=ttl_seconds),
        )
        cache.delete(cls._cache_key(sub.id, quota_key))
        return {"reservation_id": str(reservation.id), "amount": amount, "expires_at": reservation.expires_at.isoformat()}, None

    @classmethod
    def confirm_reservation(cls, reservation_id):
        try:
            r = QuotaReservation.objects.select_related("subscription").get(id=reservation_id, status="pending")
        except QuotaReservation.DoesNotExist:
            return None, "reservation_not_found"

        result, err = cls.increment(
            r.subscription.platform_id, r.subscription.subscriber_type,
            r.subscription.subscriber_id, r.quota_key, r.amount
        )
        r.status = "confirmed"
        r.resolved_at = timezone.now()
        r.save(update_fields=["status", "resolved_at"])
        return result, err

    @classmethod
    def release_reservation(cls, reservation_id):
        try:
            r = QuotaReservation.objects.select_related("subscription").get(id=reservation_id, status="pending")
        except QuotaReservation.DoesNotExist:
            return None, "reservation_not_found"

        r.status = "released"
        r.resolved_at = timezone.now()
        r.save(update_fields=["status", "resolved_at"])
        cache.delete(cls._cache_key(r.subscription.id, r.quota_key))
        return {"released": True}, None

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\quotas\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\models.py =====
`
"""AGT Subscription Service v1.0 - Modeles Subscriptions, Events, Usage, Config."""
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class SubscriptionStatus(models.TextChoices):
    PENDING_PAYMENT = "pending_payment", "Pending Payment"
    TRIAL = "trial", "Trial"
    ACTIVE = "active", "Active"
    GRACE = "grace", "Grace"
    EXPIRED = "expired", "Expired"
    SUSPENDED = "suspended", "Suspended"
    CANCELLED = "cancelled", "Cancelled"


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    subscriber_type = models.CharField(max_length=20)  # user or organization
    subscriber_id = models.UUIDField(db_index=True)
    plan = models.ForeignKey("plans.Plan", on_delete=models.PROTECT, related_name="subscriptions")
    plan_price = models.ForeignKey("plans.PlanPrice", on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.PENDING_PAYMENT, db_index=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_end = models.DateTimeField(null=True, blank=True)
    grace_end = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subscriber_type}:{self.subscriber_id} -> {self.plan.name} [{self.status}]"

    def is_usable(self):
        return self.status in [SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE, SubscriptionStatus.GRACE]

    def days_remaining(self):
        delta = self.current_period_end - timezone.now()
        return max(0, delta.days)

    def cancel(self):
        self.cancelled_at = timezone.now()
        self.cancel_at_period_end = True
        self.save(update_fields=["cancelled_at", "cancel_at_period_end", "updated_at"])

    def activate(self):
        self.status = SubscriptionStatus.ACTIVE
        self.save(update_fields=["status", "updated_at"])

    def suspend(self):
        self.status = SubscriptionStatus.SUSPENDED
        self.save(update_fields=["status", "updated_at"])


class SubscriptionQuotaUsage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="quota_usage")
    quota_key = models.CharField(max_length=50)
    used = models.IntegerField(default=0)
    overage = models.IntegerField(default=0)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscription_quotas_usage"
        unique_together = [("subscription", "quota_key", "period_start")]


class QuotaReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="reservations")
    quota_key = models.CharField(max_length=50)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="pending")  # pending, confirmed, released
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "quota_reservations"


class SubscriptionEvent(models.Model):
    EVENT_TYPES = [
        ("created", "Created"), ("activated", "Activated"), ("renewed", "Renewed"),
        ("upgraded", "Upgraded"), ("downgraded", "Downgraded"), ("cancelled", "Cancelled"),
        ("expired", "Expired"), ("suspended", "Suspended"), ("reactivated", "Reactivated"),
        ("cycle_closed", "Cycle Closed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    from_plan = models.ForeignKey("plans.Plan", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    to_plan = models.ForeignKey("plans.Plan", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    prorate_credit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    prorate_debit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscription_events"
        ordering = ["-created_at"]


class PlatformSubscriptionConfig(models.Model):
    POST_TRIAL_CHOICES = [("downgrade_to_free", "Downgrade"), ("suspend", "Suspend"), ("expire", "Expire")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(unique=True)
    default_trial_days = models.IntegerField(default=0)
    grace_period_days = models.IntegerField(default=0)
    post_trial_behavior = models.CharField(max_length=20, choices=POST_TRIAL_CHOICES, default="suspend")
    default_currency = models.CharField(max_length=3, default="XAF")
    allowed_cycles = models.JSONField(default=list)
    require_default_plan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_subscription_config"

    @classmethod
    def get_for_platform(cls, platform_id):
        try:
            return cls.objects.get(platform_id=platform_id)
        except cls.DoesNotExist:
            return cls(platform_id=platform_id, default_trial_days=0, grace_period_days=0, allowed_cycles=["monthly", "yearly"])

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\service.py =====
`
"""AGT Subscription Service v1.0 - Subscription lifecycle service."""
import logging
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from apps.plans.models import Plan, PlanPrice, PlanQuota
from apps.subscriptions.models import (
    Subscription, SubscriptionStatus, SubscriptionEvent,
    SubscriptionQuotaUsage, PlatformSubscriptionConfig,
)

logger = logging.getLogger(__name__)


class SubscriptionService:

    @classmethod
    def create(cls, platform_id, subscriber_type, subscriber_id, plan_id, billing_cycle, with_trial=False):
        # Verifier pas d'abonnement actif
        existing = Subscription.objects.filter(
            platform_id=platform_id, subscriber_type=subscriber_type,
            subscriber_id=subscriber_id
        ).exclude(status__in=["expired", "cancelled"]).first()
        if existing:
            return None, "active_subscription_exists"

        try:
            plan = Plan.objects.get(id=plan_id, platform_id=platform_id, is_active=True)
        except Plan.DoesNotExist:
            return None, "plan_not_found"

        price = PlanPrice.objects.filter(plan=plan, billing_cycle=billing_cycle, is_active=True).first()
        if not price:
            return None, "price_not_found"

        config = PlatformSubscriptionConfig.get_for_platform(str(platform_id))
        now = timezone.now()
        cycle_days = price.get_cycle_days()
        period_end = now + timedelta(days=cycle_days)

        trial_end = None
        status = SubscriptionStatus.PENDING_PAYMENT

        if plan.is_free:
            status = SubscriptionStatus.ACTIVE
        elif with_trial and config.default_trial_days > 0:
            trial_end = now + timedelta(days=config.default_trial_days)
            status = SubscriptionStatus.TRIAL

        sub = Subscription.objects.create(
            platform_id=platform_id, subscriber_type=subscriber_type,
            subscriber_id=subscriber_id, plan=plan, plan_price=price,
            status=status, current_period_start=now, current_period_end=period_end,
            trial_end=trial_end,
        )

        # Initialiser les quotas usage
        cls._init_quota_usage(sub)

        SubscriptionEvent.objects.create(subscription=sub, event_type="created",
                                          to_plan=plan, metadata={"billing_cycle": billing_cycle, "with_trial": with_trial})

        return sub, None

    @classmethod
    def activate(cls, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return None, "not_found"

        if sub.status not in [SubscriptionStatus.PENDING_PAYMENT, SubscriptionStatus.TRIAL]:
            return None, "cannot_activate"

        sub.status = SubscriptionStatus.ACTIVE
        sub.save(update_fields=["status", "updated_at"])
        SubscriptionEvent.objects.create(subscription=sub, event_type="activated")
        return sub, None

    @classmethod
    def change_plan(cls, sub_id, new_plan_id, billing_cycle):
        try:
            sub = Subscription.objects.select_related("plan", "plan_price").get(id=sub_id)
        except Subscription.DoesNotExist:
            return None, "not_found"

        if not sub.is_usable():
            return None, "subscription_not_active"

        if str(sub.plan_id) == str(new_plan_id):
            return None, "same_plan"

        try:
            new_plan = Plan.objects.get(id=new_plan_id, platform_id=sub.platform_id, is_active=True)
        except Plan.DoesNotExist:
            return None, "new_plan_not_found"

        new_price = PlanPrice.objects.filter(plan=new_plan, billing_cycle=billing_cycle, is_active=True).first()
        if not new_price:
            return None, "new_price_not_found"

        # Calcul prorata
        days_remaining = sub.days_remaining()
        old_daily = sub.plan_price.price_per_day()
        new_daily = new_price.price_per_day()

        credit = Decimal(str(days_remaining)) * old_daily
        debit = Decimal(str(days_remaining)) * new_daily
        amount_due = max(Decimal("0"), debit - credit)

        old_plan = sub.plan
        event_type = "upgraded" if new_plan.tier_order > old_plan.tier_order else "downgraded"

        # Mettre a jour
        sub.plan = new_plan
        sub.plan_price = new_price
        sub.save(update_fields=["plan", "plan_price", "updated_at"])

        SubscriptionEvent.objects.create(
            subscription=sub, event_type=event_type,
            from_plan=old_plan, to_plan=new_plan,
            prorate_credit=credit, prorate_debit=debit,
        )

        return {
            "subscription_id": str(sub.id), "old_plan": old_plan.name,
            "new_plan": new_plan.name, "event_type": event_type,
            "prorate_credit": float(credit), "prorate_debit": float(debit),
            "amount_due": float(amount_due),
        }, None

    @classmethod
    def cancel(cls, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return None, "not_found"

        if sub.status in [SubscriptionStatus.CANCELLED, SubscriptionStatus.EXPIRED]:
            return None, "already_terminated"

        sub.cancel()
        SubscriptionEvent.objects.create(subscription=sub, event_type="cancelled")
        return sub, None

    @classmethod
    def _init_quota_usage(cls, sub):
        quotas = PlanQuota.objects.filter(plan=sub.plan)
        for q in quotas:
            SubscriptionQuotaUsage.objects.get_or_create(
                subscription=sub, quota_key=q.quota_key, period_start=sub.current_period_start,
                defaults={"period_end": sub.current_period_end, "used": 0, "overage": 0}
            )

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\urls.py =====
`
from django.urls import path
from apps.subscriptions.views import (
    HealthCheckView, PlanListCreateView, PlanDetailView, PlanArchiveView,
    SubscriptionCreateView, SubscriptionListView, SubscriptionDetailView,
    SubscriptionCancelView, SubscriptionChangePlanView, SubscriptionActivateView,
    SubscriptionReactivateView, QuotaCheckView, QuotaIncrementView,
    QuotaReserveView, QuotaConfirmView, QuotaReleaseView, QuotaUsageView,
    OrganizationListCreateView, OrganizationMemberView,
    PlatformConfigView, AdminStatsView,
)

urlpatterns = [
    path("subscriptions/health", HealthCheckView.as_view()),

    # Plans
    path("subscriptions/plans", PlanListCreateView.as_view()),
    path("subscriptions/plans/<uuid:plan_id>", PlanDetailView.as_view()),
    path("subscriptions/plans/<uuid:plan_id>/archive", PlanArchiveView.as_view()),

    # Subscriptions
    path("subscriptions", SubscriptionCreateView.as_view()),
    path("subscriptions/list", SubscriptionListView.as_view()),
    path("subscriptions/<uuid:sub_id>", SubscriptionDetailView.as_view()),
    path("subscriptions/<uuid:sub_id>/cancel", SubscriptionCancelView.as_view()),
    path("subscriptions/<uuid:sub_id>/change-plan", SubscriptionChangePlanView.as_view()),
    path("subscriptions/<uuid:sub_id>/activate", SubscriptionActivateView.as_view()),
    path("subscriptions/<uuid:sub_id>/reactivate", SubscriptionReactivateView.as_view()),
    path("subscriptions/<uuid:sub_id>/usage", QuotaUsageView.as_view()),

    # Quotas S2S
    path("subscriptions/quotas/check", QuotaCheckView.as_view()),
    path("subscriptions/quotas/increment", QuotaIncrementView.as_view()),
    path("subscriptions/quotas/reserve", QuotaReserveView.as_view()),
    path("subscriptions/quotas/confirm", QuotaConfirmView.as_view()),
    path("subscriptions/quotas/release", QuotaReleaseView.as_view()),

    # Organizations
    path("organizations", OrganizationListCreateView.as_view()),
    path("organizations/<uuid:org_id>/members", OrganizationMemberView.as_view()),
    path("organizations/<uuid:org_id>/members/<uuid:user_id>", OrganizationMemberView.as_view()),

    # Config
    path("subscriptions/config/<str:platform_id>", PlatformConfigView.as_view()),

    # Admin
    path("subscriptions/admin/stats", AdminStatsView.as_view()),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\views.py =====
`
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

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\tests\test_all.py =====
`
"""AGT Subscription Service v1.0 - Tests."""
import uuid
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from apps.plans.models import Plan, PlanPrice, PlanQuota
from apps.subscriptions.models import Subscription, SubscriptionEvent, SubscriptionQuotaUsage, PlatformSubscriptionConfig
from apps.organizations.models import Organization, OrganizationMember
from apps.subscriptions.service import SubscriptionService
from apps.quotas.service import QuotaService


def make_plan(platform_id=None, name="Pro", slug=None, is_free=False, tier_order=1):
    pid = platform_id or uuid.uuid4()
    plan = Plan.objects.create(platform_id=pid, name=name, slug=slug or f"plan-{uuid.uuid4().hex[:6]}",
                                is_free=is_free, tier_order=tier_order)
    PlanPrice.objects.create(plan=plan, billing_cycle="monthly", price=15000, currency="XAF")
    PlanQuota.objects.create(plan=plan, quota_key="messages", limit_value=1000, is_cyclical=True, overage_policy="hard")
    PlanQuota.objects.create(plan=plan, quota_key="storage_mb", limit_value=500, is_cyclical=False, overage_policy="overage")
    return plan


class TestPlanModel(TestCase):
    def test_create_plan(self):
        plan = make_plan()
        self.assertTrue(plan.is_active)
        self.assertEqual(plan.prices.count(), 1)
        self.assertEqual(plan.quotas.count(), 2)

    def test_price_per_day(self):
        plan = make_plan()
        price = plan.prices.first()
        self.assertAlmostEqual(float(price.price_per_day()), 500.0, places=0)


class TestSubscriptionService(TestCase):
    def setUp(self):
        self.pid = uuid.uuid4()
        self.uid = uuid.uuid4()
        self.plan = make_plan(platform_id=self.pid)

    def test_create_subscription(self):
        sub, err = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        self.assertIsNone(err)
        self.assertEqual(sub.status, "pending_payment")

    def test_create_with_trial(self):
        PlatformSubscriptionConfig.objects.create(platform_id=self.pid, default_trial_days=14, allowed_cycles=["monthly"])
        sub, err = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly", with_trial=True)
        self.assertIsNone(err)
        self.assertEqual(sub.status, "trial")
        self.assertIsNotNone(sub.trial_end)

    def test_no_duplicate_active(self):
        SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        _, err = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        self.assertEqual(err, "active_subscription_exists")

    def test_cancel(self):
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        cancelled, err = SubscriptionService.cancel(sub.id)
        self.assertIsNone(err)
        self.assertTrue(cancelled.cancel_at_period_end)

    def test_change_plan_prorata(self):
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        premium = make_plan(platform_id=self.pid, name="Premium", tier_order=2)
        PlanPrice.objects.filter(plan=premium).update(price=30000)
        result, err = SubscriptionService.change_plan(sub.id, premium.id, "monthly")
        self.assertIsNone(err)
        self.assertEqual(result["event_type"], "upgraded")
        self.assertGreater(result["amount_due"], 0)


class TestQuotaService(TestCase):
    def setUp(self):
        self.pid = uuid.uuid4()
        self.uid = uuid.uuid4()
        self.plan = make_plan(platform_id=self.pid)
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        self.sub = sub

    def test_check_quota(self):
        result = QuotaService.check(self.pid, "user", self.uid, "messages", 1)
        self.assertTrue(result["allowed"])
        self.assertEqual(result["limit"], 1000)

    def test_increment_quota(self):
        result, err = QuotaService.increment(self.pid, "user", self.uid, "messages", 5)
        self.assertIsNone(err)
        self.assertEqual(result["used"], 5)

    def test_hard_limit(self):
        QuotaService.increment(self.pid, "user", self.uid, "messages", 1000)
        _, err = QuotaService.increment(self.pid, "user", self.uid, "messages", 1)
        self.assertEqual(err, "hard_limit_exceeded")

    def test_reserve_confirm(self):
        res, err = QuotaService.reserve(self.pid, "user", self.uid, "messages", 5)
        self.assertIsNone(err)
        result, err = QuotaService.confirm_reservation(res["reservation_id"])
        self.assertIsNone(err)
        self.assertEqual(result["used"], 5)


class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        resp = client.get("/api/v1/subscriptions/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestPlanEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    def test_create_plan(self):
        resp = self.client.post("/api/v1/subscriptions/plans", data={
            "platform_id": str(uuid.uuid4()), "name": "Starter", "slug": "starter",
            "prices": [{"billing_cycle": "monthly", "price": 5000}],
            "quotas": [{"quota_key": "max_items", "limit_value": 10}],
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_plans(self):
        make_plan()
        resp = self.client.get("/api/v1/subscriptions/plans")
        self.assertEqual(resp.status_code, 200)


class TestOrganization(TestCase):
    def test_create_org(self):
        pid = uuid.uuid4()
        org = Organization.objects.create(platform_id=pid, name="ACME", owner_user_id=uuid.uuid4())
        self.assertEqual(org.name, "ACME")

    def test_add_member(self):
        org = Organization.objects.create(platform_id=uuid.uuid4(), name="Corp", owner_user_id=uuid.uuid4())
        OrganizationMember.objects.create(organization=org, user_id=uuid.uuid4())
        self.assertEqual(org.members.count(), 1)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\apps\subscriptions\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\common\authentication.py =====
`
"""AGT Subscription Service v1.0 - Authentication JWT."""
import jwt, logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.platform_id = p.get("platform_id")
        self.is_authenticated = True

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return None
        token = h.split(" ", 1)[1]
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached:
            return JWTPayload(cached), cached
        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try:
            payload = jwt.decode(token, pk, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload

    def authenticate_header(self, request):
        return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\settings.py =====
`
"""AGT Subscription Service v1.0 - Django Settings"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes", "django.contrib.staticfiles",
    "rest_framework", "drf_spectacular", "corsheaders",
    "apps.plans", "apps.subscriptions", "apps.quotas", "apps.organizations",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
              "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]

import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/4")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL,
                       "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}

def _read_key(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
PAYMENT_SERVICE_URL = config("PAYMENT_SERVICE_URL", default="")
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", default="")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["common.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "UNAUTHENTICATED_USER": None,
}
SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Subscription Service API", "VERSION": "1.0.0",
    "DESCRIPTION": "Plans, abonnements, quotas temps reel, prorata, organisations B2B.",
    "TAGS": [{"name": "Health"}, {"name": "Plans"}, {"name": "Subscriptions"},
             {"name": "Quotas"}, {"name": "Organizations"}, {"name": "Config"}, {"name": "Admin"}],
}
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {"version": 1, "disable_existing_loggers": False,
           "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\settings_test.py =====
`
from config.settings import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
PAYMENT_SERVICE_URL = ""
NOTIFICATION_SERVICE_URL = ""
LOGGING = {"version": 1, "disable_existing_loggers": True, "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path("api/v1/", include("apps.subscriptions.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-subscription\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\.env =====
`
# ============================================================
# AGT Users Service v1.0 - Variables d'environnement
# ============================================================

# --- Django ---
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# --- Base de donnees ---
DATABASE_URL=postgresql://users_user:users_password@db:5432/agt_users_db

# --- Redis ---
REDIS_URL=redis://redis:6379/1

# --- Service Auth (validation JWT) ---
AUTH_SERVICE_URL=http://auth-service:7000/api/v1
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
AUTH_ADMIN_API_KEY=change-me-same-as-auth-admin-key

# --- Service Media ---
MEDIA_SERVICE_URL=http://media-service:7003/api/v1

# --- Service Notification ---
NOTIFICATION_SERVICE_URL=http://notification-service:7002/api/v1

# --- Cache TTL ---
PERMISSION_CACHE_TTL=300
PROFILE_CACHE_TTL=60

# --- RGPD ---
DEFAULT_HARD_DELETE_DELAY_DAYS=30

# --- CORS ---
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\.env.example =====
`
# ============================================================
# AGT Users Service v1.0 - Variables d'environnement
# ============================================================

# --- Django ---
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# --- Base de donnees ---
DATABASE_URL=postgresql://users_user:users_password@db:5432/agt_users_db

# --- Redis ---
REDIS_URL=redis://redis:6379/1

# --- Service Auth (validation JWT) ---
AUTH_SERVICE_URL=http://auth-service:7000/api/v1
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
AUTH_ADMIN_API_KEY=change-me-same-as-auth-admin-key

# --- Service Media ---
MEDIA_SERVICE_URL=http://media-service:7003/api/v1

# --- Service Notification ---
NOTIFICATION_SERVICE_URL=http://notification-service:7002/api/v1

# --- Cache TTL ---
PERMISSION_CACHE_TTL=300
PROFILE_CACHE_TTL=60

# --- RGPD ---
DEFAULT_HARD_DELETE_DELAY_DAYS=30

# --- CORS ---
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\CDC_v1.0.md =====
`
# AGT Users Service - Cahier des Charges v1.0

> Version : 1.0 | Statut : Implementation-ready | Classification : Confidentiel

## 1. Perimetre

Profils utilisateurs, RBAC dynamique, documents KYC, adresses, metadonnees, audit trail.

**Hors perimetre** : authentification (Auth), stockage fichiers (Media), envoi notifications (Notification), CRUD plateformes (Auth).

**Source de verite** : Auth = identite d'authentification. Users = profil, roles, permissions.

## 2. Convention d'identite

- `{id}` dans les endpoints = `users_profiles.id` (UUID interne Users)
- `auth_user_id` = `users_auth.id` (FK logique vers Auth)
- Les services externes utilisent `GET /api/v1/users/by-auth/{authUserId}` pour resoudre
- `platform_id` = UUID Auth directement (pas de table platforms locale)
- `email` et `phone` sont **read-only** dans Users (seul Auth modifie via sync)

## 3. Modele de donnees

### Tables principales
- `users_profiles` : profil etendu (+ hard_delete_after, purge_auth_pending, deletion_error_reason)
- `addresses` : adresses utilisateur, type libre
- `user_metadata` : cle-valeur flexible par plateforme
- `audit_logs` : tracabilite de toutes les modifications

### Tables RBAC
- `roles` : roles dynamiques par plateforme (unique: platform_id + name)
- `permissions` : permissions atomiques par plateforme
- `role_permissions` : liaison role-permission
- `user_roles` : assignation role-utilisateur (unique: user + role, sans platform redondant)

### Tables Documents
- `documents` : documents KYC avec workflow pending/validated/rejected
- `document_history` : historique des versions lors de re-soumission

## 4. Modele de suppression dual (CDC v2.1)

1. **Quitter une plateforme** : `DELETE /users/{id}/platforms/{platformId}` â€” retire roles, metadata, archive documents. Profil et Auth intacts.
2. **Soft delete global** : `DELETE /users/{id}` â€” status=deleted, hard_delete_after calcule, Auth desactive via S2S.
3. **Hard delete RGPD** : `DELETE /users/{id}/permanent` â€” sequence securisee : deletion_in_progress, purge Auth, puis purge Users.

## 5. Endpoints

Base URL : `/api/v1`
Documentation : `/api/v1/docs/` (Swagger) | `/api/v1/redoc/`

### Profil
- `POST /users` - Provisioning (par Auth)
- `GET /users` - Listing pagine
- `GET /users/{id}` - Consultation
- `PUT /users/{id}` - Mise a jour (email/phone NON modifiables)
- `DELETE /users/{id}` - Soft delete global
- `GET /users/by-auth/{authUserId}` - Lookup par auth_user_id
- `DELETE /users/{id}/platforms/{platformId}` - Quitter plateforme
- `DELETE /users/{id}/permanent` - Hard delete RGPD
- `PUT /users/{id}/photo` - Photo profil
- `GET /users/search` - Recherche
- `GET /users/stats` - Statistiques

### Sync (par Auth)
- `POST /users/status-sync` - Sync statut
- `POST /users/sync` - Sync email/phone

### Adresses
- `POST/GET /users/{id}/addresses` - CRUD
- `PUT/DELETE /users/{id}/addresses/{addressId}`
- `PUT /users/{id}/addresses/{addressId}/default`

### Roles
- `POST/GET /platforms/{platformId}/roles` - CRUD roles
- `POST/GET /platforms/{platformId}/permissions` - CRUD permissions
- `POST/DELETE /platforms/{platformId}/roles/{roleId}/permissions` - Liaison
- `POST/GET /users/{id}/roles` - Assignation
- `DELETE /users/{id}/roles/{roleId}`
- `GET /users/{id}/permissions/check` - Verification (cache Redis)

### Documents
- `POST/GET /users/{id}/documents` - Attacher/lister
- `PUT /users/{id}/documents/{docId}/status` - Valider/rejeter
- `GET /users/{id}/documents/{docId}/history` - Historique
- `DELETE /users/{id}/documents/{docId}`

### Metadata
- `PUT/GET /users/{id}/metadata/{platformId}` - Upsert/lecture
- `DELETE /users/{id}/metadata/{platformId}/{key}`

## 6. Contrats inter-services

### Auth vers Users
- Provisioning : `POST /api/v1/users`
- Sync status : `POST /api/v1/users/status-sync`
- Sync credentials : `POST /api/v1/users/sync`

### Users vers Auth
- Deactivation S2S : `POST /auth/admin/deactivate/{authUserId}`
- Purge RGPD : `DELETE /auth/admin/purge/{authUserId}`

### Users vers Notification
- Alertes : role_assigned, role_removed, document_validated, document_rejected

### Users vers Media
- Upload direct frontend, Users stocke media_id
- Suppression fichiers au hard delete

## 7. Port

Service : **7001**

---

*AG Technologies - Users Service CDC v1.0 - Confidentiel*

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_users_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: agt_users_db
      POSTGRES_USER: users_user
      POSTGRES_PASSWORD: users_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U users_user -d agt_users_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: agt_users_redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6380:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  users:
    build:
      context: .
      target: production
    container_name: agt_users_service
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://users_user:users_password@db:5432/agt_users_db
      REDIS_URL: redis://redis:6379/1
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7001:7001"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7001/api/v1/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  users-dev:
    build:
      context: .
      target: builder
    container_name: agt_users_dev
    restart: unless-stopped
    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py runserver 0.0.0.0:7001"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://users_user:users_password@db:5432/agt_users_db
      REDIS_URL: redis://redis:6379/1
      DEBUG: "True"
      DJANGO_SETTINGS_MODULE: config.settings
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7001:7001"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles:
      - dev

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7001
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7001", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\manage.py =====
`
#!/usr/bin/env python
import os, sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\README.md =====
`
# AGT Users Service - v1.0

Service de gestion des utilisateurs de l'ecosysteme AG Technologies.
Profils, RBAC dynamique, documents KYC, metadonnees, audit trail.

## Stack

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.11+ |
| Framework | Django 5.x + DRF |
| Base de donnees | PostgreSQL 15+ |
| Cache | Redis 7+ |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## Prerequisites

- Docker 24+ et Docker Compose v2
- Cle publique RSA du Service Auth (`public.pem`)

## Demarrage rapide

### Linux / macOS

```bash
bash scripts/setup.sh
```

### Windows (PowerShell)

```powershell
# 1. Ouvrir Docker Desktop et attendre qu'il soit pret (icone verte)

# 2. Autoriser l'execution des scripts (une seule fois par session)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Lancer le setup
.\scripts\setup.ps1
```

> **Prerequis** : Le Service Auth doit etre demarre en premier pour generer les cles RSA.
> Le script copie automatiquement `../agt-auth/keys/public.pem` vers `keys/auth_public.pem`.
> Si le chemin est different, copiez manuellement la cle publique.

## Documentation API (Swagger)

| URL | Description |
|-----|-------------|
| http://localhost:7001/api/v1/docs/ | Swagger UI (interactif) |
| http://localhost:7001/api/v1/redoc/ | ReDoc (lecture) |
| http://localhost:7001/api/v1/schema/ | Schema OpenAPI 3.0 (JSON) |

## Mode developpement

```bash
docker compose --profile dev up users-dev
```

## Endpoints principaux

Base URL : `http://localhost:7001/api/v1`

### Profil
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/users` | Provisioning (par Auth) |
| GET | `/users` | Listing pagine |
| GET | `/users/{id}` | Consultation profil |
| PUT | `/users/{id}` | Mise a jour (email/phone read-only) |
| DELETE | `/users/{id}` | Soft delete global |
| GET | `/users/by-auth/{authUserId}` | Lookup par auth_user_id |
| DELETE | `/users/{id}/platforms/{platformId}` | Quitter une plateforme |
| DELETE | `/users/{id}/permanent` | Hard delete RGPD |
| GET | `/users/search?q=...` | Recherche |
| GET | `/users/stats` | Statistiques |

### Sync (appeles par Auth)
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/users/status-sync` | Sync statut (inactive/active/deleted) |
| POST | `/users/sync` | Sync email/phone |

### RBAC
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/platforms/{pid}/roles` | CRUD roles |
| POST/GET | `/platforms/{pid}/permissions` | CRUD permissions |
| POST/DELETE | `/platforms/{pid}/roles/{rid}/permissions` | Liaison role-permission |
| POST/GET | `/users/{id}/roles` | Assignation roles |
| GET | `/users/{id}/permissions/check?platform_id=...&permission=...` | Verification permission |

### Documents
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/users/{id}/documents` | Attacher/lister |
| PUT | `/users/{id}/documents/{did}/status` | Valider/rejeter |
| GET | `/users/{id}/documents/{did}/history` | Historique versions |

## Tests

```bash
docker compose exec users python -m pytest -v
```

## Cahier des charges

Voir [CDC_v1.0.md](./CDC_v1.0.md) pour le cahier des charges technique complet.

## Dependances inter-services

| Service | Direction | Usage |
|---------|-----------|-------|
| **Auth** (7000) | Users vers Auth | Deactivation S2S, purge RGPD |
| **Auth** (7000) | Auth vers Users | Provisioning, sync status, sync credentials |
| **Notification** (7002) | Users vers Notif | Alertes roles, validation documents |
| **Media** (7003) | Users vers Media | Stockage photos et documents KYC |

## Variables d'environnement

Voir `.env.example` pour la liste complete.

---

*AG Technologies - Users Service v1.0 - Confidentiel*

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\requirements.txt =====
`
# Framework
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1

# Base de donnees
psycopg2-binary==2.9.9
dj-database-url==2.1.0

# Cache
django-redis==5.4.0
redis==5.0.4

# JWT (validation tokens Auth)
PyJWT==2.8.0
cryptography==42.0.5

# API Documentation (Swagger/OpenAPI 3.0)
drf-spectacular==0.27.2

# Validation
python-decouple==3.8
phonenumbers==8.13.37

# Logging
python-json-logger==2.0.7

# HTTP client (appels inter-services)
httpx==0.27.0

# Serveur WSGI
gunicorn==22.0.0

# Tests
pytest==8.2.0
pytest-django==4.8.0
factory-boy==3.3.0
faker==25.0.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\models.py =====
`
"""
AGT Users Service v1.0 - Modeles : Document, DocumentHistory.
"""
import uuid
from django.db import models
from django.utils import timezone


class DocumentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    VALIDATED = "validated", "Validated"
    REJECTED = "rejected", "Rejected"


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="documents")
    platform_id = models.UUIDField()
    doc_type = models.CharField(max_length=100)
    media_id = models.UUIDField()
    status = models.CharField(max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.PENDING)
    comment = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"
        ordering = ["-submitted_at"]

    def archive_and_resubmit(self, new_media_id):
        """Archive la version actuelle et met a jour avec le nouveau media."""
        DocumentHistory.objects.create(
            document=self,
            media_id=self.media_id,
            status=self.status,
            comment=self.comment,
            submitted_at=self.submitted_at,
            reviewed_at=self.reviewed_at,
        )
        self.media_id = new_media_id
        self.status = DocumentStatus.PENDING
        self.comment = None
        self.reviewed_at = None
        self.submitted_at = timezone.now()
        self.save()


class DocumentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="history")
    media_id = models.UUIDField()
    status = models.CharField(max_length=20)
    comment = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField()
    reviewed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_history"
        ordering = ["-archived_at"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\urls.py =====
`
from django.urls import path
from apps.documents.views import (
    DocumentListCreateView, DocumentStatusUpdateView,
    DocumentHistoryView, DocumentDeleteView,
)

urlpatterns = [
    path("users/<uuid:user_id>/documents", DocumentListCreateView.as_view(), name="documents-list-create"),
    path("users/<uuid:user_id>/documents/<uuid:doc_id>/status", DocumentStatusUpdateView.as_view(), name="document-status"),
    path("users/<uuid:user_id>/documents/<uuid:doc_id>/history", DocumentHistoryView.as_view(), name="document-history"),
    path("users/<uuid:user_id>/documents/<uuid:doc_id>", DocumentDeleteView.as_view(), name="document-delete"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\views.py =====
`
"""
AGT Users Service v1.0 - Views Documents.
"""
import logging
from django.utils import timezone
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.documents.models import Document, DocumentHistory, DocumentStatus
from apps.users.models import UserProfile
from apps.users.services import NotificationClient

logger = logging.getLogger(__name__)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "platform_id", "doc_type", "media_id", "status", "comment", "submitted_at", "reviewed_at"]


class DocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentHistory
        fields = ["id", "media_id", "status", "comment", "submitted_at", "reviewed_at", "archived_at"]


class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Attacher un document")
    def post(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        platform_id = request.data.get("platform_id")
        doc_type = request.data.get("doc_type")
        media_id = request.data.get("media_id")

        if not all([platform_id, doc_type, media_id]):
            return Response({"detail": "platform_id, doc_type et media_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Re-soumission : archiver l'ancien si existe
        existing = Document.objects.filter(user=user, platform_id=platform_id, doc_type=doc_type).first()
        if existing:
            existing.archive_and_resubmit(media_id)
            return Response(DocumentSerializer(existing).data, status=status.HTTP_200_OK)

        doc = Document.objects.create(user=user, platform_id=platform_id, doc_type=doc_type, media_id=media_id)
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Documents"], summary="Lister les documents d'un utilisateur")
    def get(self, request, user_id):
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        qs = Document.objects.filter(user_id=user_id)
        doc_type = request.GET.get("type")
        doc_status = request.GET.get("status")
        if doc_type:
            qs = qs.filter(doc_type=doc_type)
        if doc_status:
            qs = qs.filter(status=doc_status)

        return Response({"data": DocumentSerializer(qs, many=True).data})


class DocumentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Valider ou rejeter un document")
    def put(self, request, user_id, doc_id):
        try:
            doc = Document.objects.select_related("user").get(id=doc_id, user_id=user_id)
        except Document.DoesNotExist:
            return Response({"detail": "Document introuvable."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        comment = request.data.get("comment", "")

        if new_status not in ["validated", "rejected"]:
            return Response({"detail": "status doit etre 'validated' ou 'rejected'."}, status=status.HTTP_400_BAD_REQUEST)

        doc.status = new_status
        doc.comment = comment
        doc.reviewed_at = timezone.now()
        doc.save(update_fields=["status", "comment", "reviewed_at"])

        NotificationClient.notify_document_status(doc.user.email, doc.doc_type, new_status, comment)

        return Response(DocumentSerializer(doc).data)


class DocumentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Historique des versions d'un document")
    def get(self, request, user_id, doc_id):
        history = DocumentHistory.objects.filter(document_id=doc_id, document__user_id=user_id)
        return Response({"data": DocumentHistorySerializer(history, many=True).data})


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Supprimer un document")
    def delete(self, request, user_id, doc_id):
        deleted, _ = Document.objects.filter(id=doc_id, user_id=user_id).delete()
        if not deleted:
            return Response({"detail": "Document introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Document supprime."})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\documents\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\models.py =====
`
"""
AGT Users Service v1.0 - Modeles : Role, Permission, UserRole, RolePermission.
RBAC 100% dynamique. platform_id = UUID Auth directement (pas de table locale).
"""
import uuid
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"
        unique_together = [("platform_id", "name")]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permissions"
        unique_together = [("platform_id", "name")]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="role_permissions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "role_permissions"
        unique_together = [("role", "permission")]


class UserRole(models.Model):
    """CDC v2.1 : unique_together = (user, role). platform_id retire car redondant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    assigned_by = models.UUIDField(null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_roles"
        unique_together = [("user", "role")]
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.user} -> {self.role.name}"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\urls.py =====
`
from django.urls import path
from apps.roles.views import (
    RoleListCreateView, RoleDetailView,
    PermissionListCreateView, RolePermissionView,
    UserRoleListCreateView, UserRoleDeleteView, PermissionCheckView,
)

urlpatterns = [
    # Roles
    path("platforms/<uuid:platform_id>/roles", RoleListCreateView.as_view(), name="roles-list-create"),
    path("platforms/<uuid:platform_id>/roles/<uuid:role_id>", RoleDetailView.as_view(), name="roles-detail"),

    # Permissions
    path("platforms/<uuid:platform_id>/permissions", PermissionListCreateView.as_view(), name="permissions-list-create"),
    path("platforms/<uuid:platform_id>/roles/<uuid:role_id>/permissions", RolePermissionView.as_view(), name="role-permissions"),
    path("platforms/<uuid:platform_id>/roles/<uuid:role_id>/permissions/<uuid:perm_id>", RolePermissionView.as_view(), name="role-permission-detail"),

    # User Roles
    path("users/<uuid:user_id>/roles", UserRoleListCreateView.as_view(), name="user-roles"),
    path("users/<uuid:user_id>/roles/<uuid:role_id>", UserRoleDeleteView.as_view(), name="user-role-delete"),

    # Permission Check
    path("users/<uuid:user_id>/permissions/check", PermissionCheckView.as_view(), name="permission-check"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\views.py =====
`
"""
AGT Users Service v1.0 - Views : Roles, Permissions, UserRoles, PermissionCheck.
RBAC 100% dynamique. platform_id = UUID Auth directement.
"""
import logging
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.roles.models import Role, Permission, RolePermission, UserRole
from apps.users.models import UserProfile
from apps.users.services import PermissionCacheService, NotificationClient

logger = logging.getLogger(__name__)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "platform_id", "name", "description", "created_at"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "platform_id", "name", "description", "created_at"]


# --- Roles CRUD ---

class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Roles"], summary="Creer un role pour une plateforme")
    def post(self, request, platform_id):
        name = request.data.get("name")
        description = request.data.get("description", "")
        if not name:
            return Response({"detail": "name requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Role.objects.filter(platform_id=platform_id, name=name).exists():
            return Response({"detail": "Role existe deja."}, status=status.HTTP_409_CONFLICT)

        role = Role.objects.create(platform_id=platform_id, name=name, description=description)
        return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Roles"], summary="Lister les roles d'une plateforme")
    def get(self, request, platform_id):
        roles = Role.objects.filter(platform_id=platform_id)
        return Response({"data": RoleSerializer(roles, many=True).data})


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Roles"], summary="Modifier un role")
    def put(self, request, platform_id, role_id):
        try:
            role = Role.objects.get(id=role_id, platform_id=platform_id)
        except Role.DoesNotExist:
            return Response({"detail": "Role introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if "name" in request.data:
            role.name = request.data["name"]
        if "description" in request.data:
            role.description = request.data["description"]
        role.save()
        return Response(RoleSerializer(role).data)

    @extend_schema(tags=["Roles"], summary="Supprimer un role")
    def delete(self, request, platform_id, role_id):
        deleted, _ = Role.objects.filter(id=role_id, platform_id=platform_id).delete()
        if not deleted:
            return Response({"detail": "Role introuvable."}, status=status.HTTP_404_NOT_FOUND)
        PermissionCacheService.invalidate_role(str(role_id))
        return Response({"message": "Role supprime."})


# --- Permissions CRUD ---

class PermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Permissions"], summary="Creer une permission")
    def post(self, request, platform_id):
        name = request.data.get("name")
        description = request.data.get("description", "")
        if not name:
            return Response({"detail": "name requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Permission.objects.filter(platform_id=platform_id, name=name).exists():
            return Response({"detail": "Permission existe deja."}, status=status.HTTP_409_CONFLICT)

        perm = Permission.objects.create(platform_id=platform_id, name=name, description=description)
        return Response(PermissionSerializer(perm).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Permissions"], summary="Lister les permissions d'une plateforme")
    def get(self, request, platform_id):
        perms = Permission.objects.filter(platform_id=platform_id)
        return Response({"data": PermissionSerializer(perms, many=True).data})


# --- Role-Permission liaison ---

class RolePermissionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Roles"], summary="Attacher une permission a un role")
    def post(self, request, platform_id, role_id):
        perm_id = request.data.get("permission_id")
        if not perm_id:
            return Response({"detail": "permission_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(id=role_id, platform_id=platform_id)
            perm = Permission.objects.get(id=perm_id, platform_id=platform_id)
        except (Role.DoesNotExist, Permission.DoesNotExist):
            return Response({"detail": "Role ou permission introuvable."}, status=status.HTTP_404_NOT_FOUND)

        _, created = RolePermission.objects.get_or_create(role=role, permission=perm)
        PermissionCacheService.invalidate_role(str(role_id))

        if created:
            return Response({"message": "Permission attachee."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Permission deja attachee."})

    @extend_schema(tags=["Roles"], summary="Detacher une permission d'un role")
    def delete(self, request, platform_id, role_id, perm_id):
        deleted, _ = RolePermission.objects.filter(role_id=role_id, permission_id=perm_id).delete()
        if not deleted:
            return Response({"detail": "Liaison introuvable."}, status=status.HTTP_404_NOT_FOUND)
        PermissionCacheService.invalidate_role(str(role_id))
        return Response({"message": "Permission detachee."})


# --- User Roles ---

class UserRoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["User Roles"], summary="Assigner un role a un utilisateur")
    def post(self, request, user_id):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response({"detail": "role_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
        except (UserProfile.DoesNotExist, Role.DoesNotExist):
            return Response({"detail": "Utilisateur ou role introuvable."}, status=status.HTTP_404_NOT_FOUND)

        assigned_by = getattr(request.user, "auth_user_id", None)
        _, created = UserRole.objects.get_or_create(user=user, role=role, defaults={"assigned_by": assigned_by})

        if created:
            NotificationClient.notify_role_assigned(user.email, role.name, str(role.platform_id))

        return Response({
            "user_id": str(user.id),
            "role": RoleSerializer(role).data,
            "assigned": created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @extend_schema(tags=["User Roles"], summary="Lister les roles d'un utilisateur")
    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        qs = UserRole.objects.filter(user=user).select_related("role")
        platform_filter = request.GET.get("platform_id")
        if platform_filter:
            qs = qs.filter(role__platform_id=platform_filter)

        roles = []
        for ur in qs:
            roles.append({
                "role": {"id": str(ur.role.id), "name": ur.role.name, "platform_id": str(ur.role.platform_id)},
                "assigned_at": ur.assigned_at.isoformat(),
                "assigned_by": str(ur.assigned_by) if ur.assigned_by else None,
            })

        return Response({"user_id": str(user.id), "roles": roles})


class UserRoleDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["User Roles"], summary="Retirer un role a un utilisateur")
    def delete(self, request, user_id, role_id):
        deleted, _ = UserRole.objects.filter(user_id=user_id, role_id=role_id).delete()
        if not deleted:
            return Response({"detail": "Assignation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        PermissionCacheService.invalidate_user_platform(str(user_id), "")
        return Response({"message": "Role retire."})


# --- Permission Check ---

class PermissionCheckView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Permissions"], summary="Verifier une permission (cache Redis)")
    def get(self, request, user_id):
        platform_id = request.GET.get("platform_id")
        perm_name = request.GET.get("permission")

        if not platform_id or not perm_name:
            return Response({"detail": "platform_id et permission requis."}, status=status.HTTP_400_BAD_REQUEST)

        cached = PermissionCacheService.get(str(user_id), platform_id, perm_name)
        if cached is not None:
            return Response(cached)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user_roles = UserRole.objects.filter(user=user, role__platform_id=platform_id).select_related("role")

        granted = False
        via_role = None

        for ur in user_roles:
            has_perm = RolePermission.objects.filter(
                role=ur.role, permission__name=perm_name, permission__platform_id=platform_id,
            ).exists()
            if has_perm:
                granted = True
                via_role = ur.role.name
                break

        result = {
            "user_id": str(user_id), "platform_id": platform_id,
            "permission": perm_name, "granted": granted, "via_role": via_role,
        }
        PermissionCacheService.set(str(user_id), platform_id, perm_name, result)
        return Response(result)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\roles\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\authentication.py =====
`
"""
AGT Users Service v1.0 - Authentification JWT.
Valide les tokens emis par Auth via cle publique RS256 (pas d'appel reseau).
"""
import logging
import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JWTPayload:
    def __init__(self, payload):
        self.payload = payload
        self.id = payload.get("sub")
        self.auth_user_id = payload.get("sub")
        self.email = payload.get("email")
        self.platform_id = payload.get("platform_id")
        self.session_id = payload.get("session_id")
        self.is_authenticated = True

    def __str__(self):
        return f"JWTUser({self.auth_user_id})"


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1]

        cache_key = f"jwt_decoded:{token[:32]}"
        cached = cache.get(cache_key)
        if cached:
            return JWTPayload(cached), cached

        public_key = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not public_key:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")

        try:
            payload = jwt.decode(token, public_key, algorithms=["RS256"],
                                 audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})

        cache.set(cache_key, payload, timeout=30)
        return JWTPayload(payload), payload

    def authenticate_header(self, request):
        return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\exceptions.py =====
`
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(response.data, dict) and "detail" not in response.data:
            response.data = {"detail": response.data}
        elif isinstance(response.data, list):
            response.data = {"detail": response.data}
    else:
        logger.exception("Unhandled exception", exc_info=exc)
        response = Response(
            {"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Erreur interne du serveur."}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\models.py =====
`
"""
AGT Users Service v1.0 - Modeles Django
Conforme CDC Users v2.1 : profils, adresses, metadata, audit_logs.
Plus de table platforms locale - platform_id = UUID Auth directement.
"""
import uuid
from django.db import models
from django.utils import timezone


class UserStatusChoice(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DELETED = "deleted", "Deleted"
    DELETION_IN_PROGRESS = "deletion_in_progress", "Deletion In Progress"


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_user_id = models.UUIDField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=255, null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.CharField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=30, choices=UserStatusChoice.choices, default=UserStatusChoice.ACTIVE, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    hard_delete_after = models.DateTimeField(null=True, blank=True)
    purge_auth_pending = models.BooleanField(default=False)
    deletion_error_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email or self.auth_user_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def soft_delete(self, hard_delete_delay_days=None):
        from django.conf import settings
        delay = hard_delete_delay_days or getattr(settings, "DEFAULT_HARD_DELETE_DELAY_DAYS", 30)
        self.status = UserStatusChoice.DELETED
        self.deleted_at = timezone.now()
        self.hard_delete_after = timezone.now() + timezone.timedelta(days=delay)
        self.save(update_fields=["status", "deleted_at", "hard_delete_after", "updated_at"])

    def hard_delete(self):
        self.delete()

    def is_active_user(self):
        return self.status == UserStatusChoice.ACTIVE


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="addresses")
    type = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addresses"
        ordering = ["-is_default", "-created_at"]

    def set_as_default(self):
        Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        self.is_default = True
        self.save(update_fields=["is_default"])


class UserMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="metadata")
    platform_id = models.UUIDField()
    key = models.CharField(max_length=100)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_metadata"
        unique_together = [("user", "platform_id", "key")]
        ordering = ["key"]


class AuditLog(models.Model):
    ACTOR_TYPE_CHOICES = [
        ("user", "User"), ("service", "Service"), ("system", "System"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=50)
    entity_id = models.UUIDField()
    action = models.CharField(max_length=30)
    actor_id = models.UUIDField(null=True, blank=True)
    actor_type = models.CharField(max_length=20, choices=ACTOR_TYPE_CHOICES, default="user")
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["actor_id"]),
            models.Index(fields=["created_at"]),
        ]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\pagination.py =====
`
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "page": self.page.number,
            "limit": self.get_page_size(self.request),
            "total": self.page.paginator.count,
        })

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\serializers.py =====
`
"""
AGT Users Service v1.0 - Serializers.
CDC v2.1 : email/phone read-only (seul Auth peut modifier via sync).
"""
from rest_framework import serializers
from apps.users.models import UserProfile, Address, UserMetadata


class UserProfileCreateSerializer(serializers.Serializer):
    auth_user_id = serializers.UUIDField()
    first_name = serializers.CharField(max_length=100, required=False, default="")
    last_name = serializers.CharField(max_length=100, required=False, default="")
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)

    def validate_auth_user_id(self, value):
        if UserProfile.objects.filter(auth_user_id=value).exists():
            raise serializers.ValidationError("Profil existant pour ce auth_user_id.")
        return value


class UserProfileUpdateSerializer(serializers.Serializer):
    """CDC v2.1 : email et phone NON modifiables ici."""
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(max_length=20, required=False, allow_null=True)


class UserProfileResponseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id", "auth_user_id", "first_name", "last_name", "full_name",
            "email", "phone", "avatar_url", "birth_date", "gender",
            "status", "created_at", "updated_at",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserProfileMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "auth_user_id", "first_name", "last_name", "email", "status", "created_at"]


class StatusSyncSerializer(serializers.Serializer):
    auth_user_id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=["active", "inactive", "deleted"])


class CredentialsSyncSerializer(serializers.Serializer):
    auth_user_id = serializers.UUIDField()
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)


class AddressCreateSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20, required=False, allow_null=True)
    is_default = serializers.BooleanField(default=False)


class AddressUpdateSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50, required=False)
    street = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, required=False)
    postal_code = serializers.CharField(max_length=20, required=False, allow_null=True)


class AddressResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "type", "street", "city", "country", "postal_code", "is_default", "created_at"]


class UserMetadataResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMetadata
        fields = ["key", "value", "updated_at"]


class PhotoUpdateSerializer(serializers.Serializer):
    media_id = serializers.UUIDField()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\services.py =====
`
"""
AGT Users Service v1.0 - Services : Cache, Notification, Auth client.
"""
import logging
import uuid
import httpx
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class PermissionCacheService:
    @staticmethod
    def _key(user_id, platform_id, perm_name):
        return f"perm:{user_id}:{platform_id}:{perm_name}"

    @classmethod
    def get(cls, user_id, platform_id, perm_name):
        return cache.get(cls._key(user_id, platform_id, perm_name))

    @classmethod
    def set(cls, user_id, platform_id, perm_name, result):
        cache.set(cls._key(user_id, platform_id, perm_name), result, timeout=getattr(settings, "PERMISSION_CACHE_TTL", 300))

    @classmethod
    def invalidate_user_platform(cls, user_id, platform_id):
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            keys = conn.keys(f"perm:{user_id}:{platform_id}:*")
            if keys:
                conn.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache invalidation failed: {e}")

    @classmethod
    def invalidate_role(cls, role_id):
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            keys = conn.keys("perm:*")
            if keys:
                conn.delete(*keys)
        except Exception as e:
            logger.warning(f"Role cache invalidation failed: {e}")


class ProfileCacheService:
    @staticmethod
    def _key(user_id):
        return f"profile:{user_id}"

    @classmethod
    def get(cls, user_id):
        return cache.get(cls._key(user_id))

    @classmethod
    def set(cls, user_id, data):
        cache.set(cls._key(user_id), data, timeout=getattr(settings, "PROFILE_CACHE_TTL", 60))

    @classmethod
    def invalidate(cls, user_id):
        cache.delete(cls._key(user_id))


class NotificationClient:
    @staticmethod
    def send(notification_type, recipient, template, data):
        url = getattr(settings, "NOTIFICATION_SERVICE_URL", "")
        if not url:
            return False
        try:
            resp = httpx.post(f"{url}/notifications/send", json={
                "type": notification_type, "recipient": recipient,
                "template": template, "data": data,
                "idempotency_key": str(uuid.uuid4()),
            }, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Notification error: {e}")
            return False

    @classmethod
    def notify_role_assigned(cls, user_email, role_name, platform_name):
        cls.send("role_assigned", {"email": user_email}, "users_role_assigned",
                 {"role_name": role_name, "platform_name": platform_name})

    @classmethod
    def notify_document_status(cls, user_email, doc_type, doc_status, comment=None):
        cls.send("document_status_update", {"email": user_email}, "users_document_status",
                 {"doc_type": doc_type, "status": doc_status, "comment": comment})


class AuthServiceClient:
    @staticmethod
    def deactivate_user(auth_user_id):
        url = getattr(settings, "AUTH_SERVICE_URL", "")
        admin_key = getattr(settings, "AUTH_ADMIN_API_KEY", "")
        if not url:
            logger.warning("AUTH_SERVICE_URL non configure")
            return False
        try:
            resp = httpx.post(
                f"{url}/auth/admin/deactivate/{auth_user_id}",
                headers={"X-Admin-API-Key": admin_key},
                timeout=5.0,
            )
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Auth deactivate failed: {e}")
            return False

    @staticmethod
    def purge_user(auth_user_id):
        url = getattr(settings, "AUTH_SERVICE_URL", "")
        admin_key = getattr(settings, "AUTH_ADMIN_API_KEY", "")
        if not url:
            return False
        try:
            resp = httpx.delete(
                f"{url}/auth/admin/purge/{auth_user_id}",
                headers={"X-Admin-API-Key": admin_key},
                timeout=10.0,
            )
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Auth purge failed: {e}")
            return False

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\urls.py =====
`
from django.urls import path
from apps.users.views import (
    HealthCheckView, UserListCreateView, UserDetailView, UserByAuthView,
    UserLeavePlatformView, UserPermanentDeleteView, UserPhotoView,
    UserSearchView, UserStatsView, StatusSyncView, CredentialsSyncView,
    AddressListCreateView, AddressDetailView, AddressSetDefaultView,
    UserMetadataView, UserMetadataKeyDeleteView,
)

urlpatterns = [
    path("health", HealthCheckView.as_view(), name="health"),

    # Profil
    path("users", UserListCreateView.as_view(), name="users-list-create"),
    path("users/search", UserSearchView.as_view(), name="users-search"),
    path("users/stats", UserStatsView.as_view(), name="users-stats"),
    path("users/status-sync", StatusSyncView.as_view(), name="users-status-sync"),
    path("users/sync", CredentialsSyncView.as_view(), name="users-sync"),
    path("users/by-auth/<uuid:auth_user_id>", UserByAuthView.as_view(), name="users-by-auth"),
    path("users/<uuid:user_id>", UserDetailView.as_view(), name="users-detail"),
    path("users/<uuid:user_id>/permanent", UserPermanentDeleteView.as_view(), name="users-permanent-delete"),
    path("users/<uuid:user_id>/photo", UserPhotoView.as_view(), name="users-photo"),
    path("users/<uuid:user_id>/platforms/<uuid:platform_id>", UserLeavePlatformView.as_view(), name="users-leave-platform"),

    # Adresses
    path("users/<uuid:user_id>/addresses", AddressListCreateView.as_view(), name="users-addresses"),
    path("users/<uuid:user_id>/addresses/<uuid:address_id>", AddressDetailView.as_view(), name="users-address-detail"),
    path("users/<uuid:user_id>/addresses/<uuid:address_id>/default", AddressSetDefaultView.as_view(), name="users-address-default"),

    # Metadata
    path("users/<uuid:user_id>/metadata/<str:platform_id>", UserMetadataView.as_view(), name="users-metadata"),
    path("users/<uuid:user_id>/metadata/<str:platform_id>/<str:key>", UserMetadataKeyDeleteView.as_view(), name="users-metadata-key"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\views.py =====
`
"""
AGT Users Service v1.0 - Views : Profil, Adresses, Metadata, Sync, Stats.
CDC v2.1 : by-auth lookup, leave platform, hard delete securise.
"""
import logging
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.users.models import UserProfile, Address, UserMetadata, UserStatusChoice, AuditLog
from apps.users.pagination import StandardPagination
from apps.users.serializers import (
    UserProfileCreateSerializer, UserProfileUpdateSerializer,
    UserProfileResponseSerializer, UserProfileMinimalSerializer,
    AddressCreateSerializer, AddressUpdateSerializer, AddressResponseSerializer,
    UserMetadataResponseSerializer, PhotoUpdateSerializer,
    StatusSyncSerializer, CredentialsSyncSerializer,
)
from apps.users.services import ProfileCacheService, NotificationClient, AuthServiceClient

logger = logging.getLogger(__name__)


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
        return Response({
            "status": "healthy" if db_ok and redis_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "version": "1.0.0",
        }, status=code)


# --- Profil CRUD ---

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Provisioning profil (par Auth)")
    def post(self, request):
        """POST /users - Provisioning (appele par Auth apres inscription)."""
        serializer = UserProfileCreateSerializer(data=request.data)
        if not serializer.is_valid():
            if "auth_user_id" in serializer.errors:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = UserProfile.objects.create(
            auth_user_id=data["auth_user_id"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
        )
        return Response(UserProfileResponseSerializer(user).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Profile"], summary="Listing pagine avec filtres")
    def get(self, request):
        """GET /users - Listing pagine avec filtres."""
        qs = UserProfile.objects.all()

        status_filter = request.GET.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        platform = request.GET.get("platform_id")
        role = request.GET.get("role")
        if platform or role:
            from apps.roles.models import UserRole
            ur_qs = UserRole.objects.all()
            if platform:
                ur_qs = ur_qs.filter(role__platform_id=platform)
            if role:
                ur_qs = ur_qs.filter(role__name=role)
            user_ids = ur_qs.values_list("user_id", flat=True)
            qs = qs.filter(id__in=user_ids)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(UserProfileMinimalSerializer(page, many=True).data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Consultation profil")
    def get(self, request, user_id):
        """GET /users/{id}"""
        cached = ProfileCacheService.get(str(user_id))
        if cached:
            return Response(cached)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        data = UserProfileResponseSerializer(user).data
        ProfileCacheService.set(str(user_id), data)
        return Response(data)

    @extend_schema(tags=["Profile"], summary="Mise a jour profil (email/phone read-only)")
    def put(self, request, user_id):
        """PUT /users/{id} - email/phone NON modifiables (CDC v2.1)."""
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        old_values = {}
        for field, value in serializer.validated_data.items():
            old_values[field] = getattr(user, field)
            setattr(user, field, value)

        user.save(update_fields=list(serializer.validated_data.keys()) + ["updated_at"])
        ProfileCacheService.invalidate(str(user_id))

        AuditLog.objects.create(
            entity_type="users_profiles", entity_id=user.id, action="update",
            actor_id=getattr(request.user, "auth_user_id", None), actor_type="user",
            old_value=old_values, new_value=serializer.validated_data,
        )

        return Response(UserProfileResponseSerializer(user).data)

    @extend_schema(tags=["Profile"], summary="Soft delete global")
    def delete(self, request, user_id):
        """DELETE /users/{id} - Soft delete global + deactivate Auth."""
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.soft_delete()
        ProfileCacheService.invalidate(str(user_id))

        # Propager deactivation vers Auth (CDC v2.1 : S2S sans mot de passe)
        AuthServiceClient.deactivate_user(str(user.auth_user_id))

        AuditLog.objects.create(
            entity_type="users_profiles", entity_id=user.id, action="soft_delete",
            actor_id=getattr(request.user, "auth_user_id", None),
        )

        return Response({
            "message": "Account deactivated",
            "status": "deleted",
            "hard_delete_scheduled": user.hard_delete_after.isoformat() if user.hard_delete_after else None,
        })


class UserByAuthView(APIView):
    """GET /users/by-auth/{authUserId} - Lookup par auth_user_id (CDC v2.1)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Lookup par auth_user_id")
    def get(self, request, auth_user_id):
        try:
            user = UserProfile.objects.get(auth_user_id=auth_user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProfileResponseSerializer(user).data)


class UserLeavePlatformView(APIView):
    """DELETE /users/{id}/platforms/{platformId} - Quitter une plateforme (CDC v2.1)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Quitter une plateforme")
    def delete(self, request, user_id, platform_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        from apps.roles.models import UserRole
        roles_removed = UserRole.objects.filter(user=user, role__platform_id=platform_id).delete()[0]

        metadata_cleared = UserMetadata.objects.filter(user=user, platform_id=platform_id).delete()[0] > 0

        from apps.documents.models import Document
        docs_archived = Document.objects.filter(user=user, platform_id=platform_id).update(
            status="archived"
        )

        AuditLog.objects.create(
            entity_type="users_profiles", entity_id=user.id, action="leave_platform",
            actor_id=getattr(request.user, "auth_user_id", None),
            new_value={"platform_id": str(platform_id), "roles_removed": roles_removed},
        )

        return Response({
            "message": "Platform left",
            "platform_id": str(platform_id),
            "roles_removed": roles_removed,
            "metadata_cleared": metadata_cleared,
            "documents_archived": docs_archived,
        })


class UserPermanentDeleteView(APIView):
    """DELETE /users/{id}/permanent - Hard delete RGPD securise (CDC v2.1)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Hard delete RGPD")
    def delete(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Etape 1 : marquer deletion_in_progress
        user.status = UserStatusChoice.DELETION_IN_PROGRESS
        user.save(update_fields=["status", "updated_at"])

        # Etape 2 : purge Auth
        auth_purged = AuthServiceClient.purge_user(str(user.auth_user_id))

        if not auth_purged:
            user.purge_auth_pending = True
            user.deletion_error_reason = "Auth purge failed - will retry"
            user.save(update_fields=["purge_auth_pending", "deletion_error_reason", "updated_at"])
            return Response({
                "detail": "Purge Auth echouee. Retry planifie.",
                "purge_auth_pending": True,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Etape 3 : purge Users
        ProfileCacheService.invalidate(str(user_id))
        user.hard_delete()

        return Response({"message": "Compte supprime definitivement (RGPD)."})


class UserPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Mise a jour photo profil")
    def put(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhotoUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user.avatar_url = f"media://{serializer.validated_data['media_id']}"
        user.save(update_fields=["avatar_url", "updated_at"])
        ProfileCacheService.invalidate(str(user_id))
        return Response(UserProfileResponseSerializer(user).data)


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Recherche utilisateurs")
    def get(self, request):
        q = request.GET.get("q", "").strip()
        if not q:
            return Response({"detail": "Parametre 'q' requis."}, status=status.HTTP_400_BAD_REQUEST)

        qs = UserProfile.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(email__icontains=q) | Q(phone__icontains=q)
        ).exclude(status=UserStatusChoice.DELETED)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(UserProfileMinimalSerializer(page, many=True).data)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Statistiques globales")
    def get(self, request):
        from apps.roles.models import UserRole
        total = UserProfile.objects.count()
        by_status = dict(UserProfile.objects.values_list("status").annotate(count=Count("id")))

        return Response({
            "total_users": total,
            "by_status": {
                "active": by_status.get("active", 0),
                "inactive": by_status.get("inactive", 0),
                "deleted": by_status.get("deleted", 0),
            },
        })


# --- Sync endpoints (appeles par Service Auth) ---

class StatusSyncView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Sync"], summary="Sync statut depuis Auth")
    def post(self, request):
        serializer = StatusSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserProfile.objects.get(auth_user_id=data["auth_user_id"])
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        new_status = data["status"]
        if new_status == "inactive":
            user.status = UserStatusChoice.INACTIVE
        elif new_status == "active":
            user.status = UserStatusChoice.ACTIVE
        elif new_status == "deleted":
            user.soft_delete()
            return Response({"message": "Statut synchronise.", "status": new_status})

        user.save(update_fields=["status", "updated_at"])
        ProfileCacheService.invalidate(str(user.id))
        return Response({"message": "Statut synchronise.", "status": new_status})


class CredentialsSyncView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Sync"], summary="Sync email/phone depuis Auth")
    def post(self, request):
        serializer = CredentialsSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserProfile.objects.get(auth_user_id=data["auth_user_id"])
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        updated = []
        if data.get("email"):
            user.email = data["email"]
            updated.append("email")
        if data.get("phone"):
            user.phone = data["phone"]
            updated.append("phone")

        if updated:
            user.save(update_fields=updated + ["updated_at"])
            ProfileCacheService.invalidate(str(user.id))

        return Response({"message": "Identifiants synchronises."})


# --- Adresses ---

class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"], summary="Ajouter une adresse")
    def post(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address = Address.objects.create(user=user, **serializer.validated_data)
        if serializer.validated_data.get("is_default"):
            address.set_as_default()

        return Response(AddressResponseSerializer(address).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Addresses"], summary="Lister les adresses")
    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
        addresses = Address.objects.filter(user=user)
        return Response({"data": AddressResponseSerializer(addresses, many=True).data})


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"], summary="Modifier une adresse")
    def put(self, request, user_id, address_id):
        try:
            address = Address.objects.get(id=address_id, user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Adresse introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for field, value in serializer.validated_data.items():
            setattr(address, field, value)
        address.save()
        return Response(AddressResponseSerializer(address).data)

    @extend_schema(tags=["Addresses"], summary="Supprimer une adresse")
    def delete(self, request, user_id, address_id):
        try:
            address = Address.objects.get(id=address_id, user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Adresse introuvable."}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "Adresse supprimee."})


class AddressSetDefaultView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"], summary="Definir adresse par defaut")
    def put(self, request, user_id, address_id):
        try:
            address = Address.objects.get(id=address_id, user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Adresse introuvable."}, status=status.HTTP_404_NOT_FOUND)
        address.set_as_default()
        return Response({"message": "Adresse par defaut mise a jour.", "id": str(address.id)})


# --- Metadata ---

class UserMetadataView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Metadata"], summary="Upsert metadata")
    def put(self, request, user_id, platform_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(request.data, dict):
            return Response({"detail": "Body JSON (objet) requis."}, status=status.HTTP_400_BAD_REQUEST)

        upserted = []
        for key, value in request.data.items():
            UserMetadata.objects.update_or_create(
                user=user, platform_id=platform_id, key=key,
                defaults={"value": str(value)},
            )
            upserted.append({"key": key, "value": str(value)})

        return Response({"platform_id": platform_id, "metadata": upserted})

    @extend_schema(tags=["Metadata"], summary="Lire metadata par plateforme")
    def get(self, request, user_id, platform_id):
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        metadata = UserMetadata.objects.filter(user_id=user_id, platform_id=platform_id)
        result = {m.key: m.value for m in metadata}
        return Response({"user_id": str(user_id), "platform_id": platform_id, "metadata": result})


class UserMetadataKeyDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Metadata"], summary="Supprimer une cle metadata")
    def delete(self, request, user_id, platform_id, key):
        deleted, _ = UserMetadata.objects.filter(user_id=user_id, platform_id=platform_id, key=key).delete()
        if not deleted:
            return Response({"detail": "Cle introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": f"Cle '{key}' supprimee."})

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\tests\test_all.py =====
`
"""
AGT Users Service v1.0 - Tests unitaires et integration.
"""
import uuid
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import UserProfile, Address, UserMetadata, UserStatusChoice, AuditLog
from apps.roles.models import Role, Permission, RolePermission, UserRole


def make_user(**kwargs):
    defaults = {
        "auth_user_id": uuid.uuid4(),
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": f"jean_{uuid.uuid4().hex[:6]}@agt.com",
    }
    defaults.update(kwargs)
    return UserProfile.objects.create(**defaults)


def make_role(platform_id=None, name="vendeur"):
    pid = platform_id or uuid.uuid4()
    return Role.objects.create(platform_id=pid, name=name, description=f"Role {name}")


def make_permission(platform_id=None, name="create_product"):
    pid = platform_id or uuid.uuid4()
    return Permission.objects.create(platform_id=pid, name=name, description=f"Perm {name}")


# --- Modeles ---

class TestUserProfileModel(TestCase):
    def test_create_user(self):
        user = make_user()
        self.assertEqual(user.status, UserStatusChoice.ACTIVE)
        self.assertIsNotNone(user.auth_user_id)

    def test_soft_delete(self):
        user = make_user()
        user.soft_delete()
        user.refresh_from_db()
        self.assertEqual(user.status, UserStatusChoice.DELETED)
        self.assertIsNotNone(user.deleted_at)
        self.assertIsNotNone(user.hard_delete_after)

    def test_hard_delete(self):
        user = make_user()
        uid = user.id
        user.hard_delete()
        self.assertFalse(UserProfile.objects.filter(id=uid).exists())

    def test_full_name(self):
        user = make_user(first_name="Marie", last_name="Curie")
        self.assertEqual(user.get_full_name(), "Marie Curie")


class TestAddressModel(TestCase):
    def test_set_default(self):
        user = make_user()
        a1 = Address.objects.create(user=user, type="home", street="Rue 1", city="Yaounde", country="Cameroun", is_default=True)
        a2 = Address.objects.create(user=user, type="work", street="Rue 2", city="Douala", country="Cameroun")
        a2.set_as_default()
        a1.refresh_from_db()
        a2.refresh_from_db()
        self.assertFalse(a1.is_default)
        self.assertTrue(a2.is_default)


class TestRBACModel(TestCase):
    def test_role_permission_link(self):
        pid = uuid.uuid4()
        role = make_role(platform_id=pid)
        perm = make_permission(platform_id=pid)
        RolePermission.objects.create(role=role, permission=perm)
        self.assertEqual(RolePermission.objects.filter(role=role).count(), 1)

    def test_user_role_unique(self):
        user = make_user()
        role = make_role()
        UserRole.objects.create(user=user, role=role)
        # Doublon doit echouer
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(user=user, role=role)


# --- Endpoints ---

class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        response = client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["version"], "1.0.0")


class TestUserCRUD(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Simuler un JWT valide en bypassant l'auth
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "auth_user_id": str(uuid.uuid4())})())

    def test_create_user_provisioning(self):
        response = self.client.post("/api/v1/users", data={
            "auth_user_id": str(uuid.uuid4()),
            "first_name": "Test",
            "last_name": "User",
            "email": "test@agt.com",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_create_duplicate(self):
        auth_id = str(uuid.uuid4())
        make_user(auth_user_id=auth_id)
        response = self.client.post("/api/v1/users", data={
            "auth_user_id": auth_id,
            "email": "other@agt.com",
        }, format="json")
        self.assertEqual(response.status_code, 409)

    def test_get_user(self):
        user = make_user()
        response = self.client.get(f"/api/v1/users/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["auth_user_id"], str(user.auth_user_id))

    def test_update_user(self):
        user = make_user()
        response = self.client.put(f"/api/v1/users/{user.id}", data={
            "first_name": "Updated",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["first_name"], "Updated")

    def test_by_auth_lookup(self):
        user = make_user()
        response = self.client.get(f"/api/v1/users/by-auth/{user.auth_user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(user.id))

    @patch("apps.users.services.AuthServiceClient.deactivate_user", return_value=True)
    def test_soft_delete(self, mock_deactivate):
        user = make_user()
        response = self.client.delete(f"/api/v1/users/{user.id}")
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.status, UserStatusChoice.DELETED)
        mock_deactivate.assert_called_once()


class TestStatusSync(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "auth_user_id": str(uuid.uuid4())})())

    def test_status_sync_inactive(self):
        user = make_user()
        response = self.client.post("/api/v1/users/status-sync", data={
            "auth_user_id": str(user.auth_user_id),
            "status": "inactive",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.status, UserStatusChoice.INACTIVE)

    def test_credentials_sync(self):
        user = make_user()
        response = self.client.post("/api/v1/users/sync", data={
            "auth_user_id": str(user.auth_user_id),
            "email": "new@agt.com",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.email, "new@agt.com")


class TestLeavePlatform(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "auth_user_id": str(uuid.uuid4())})())

    def test_leave_platform(self):
        user = make_user()
        pid = uuid.uuid4()
        role = Role.objects.create(platform_id=pid, name="vendeur")
        UserRole.objects.create(user=user, role=role)
        UserMetadata.objects.create(user=user, platform_id=pid, key="shop", value="Test")

        response = self.client.delete(f"/api/v1/users/{user.id}/platforms/{pid}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["roles_removed"], 1)
        self.assertTrue(data["metadata_cleared"])

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\apps\users\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\common\middleware.py =====
`
# AGT Users Service v1.0 - Middleware placeholder
# Rate limiting sera ajoute si necessaire en v1.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\settings.py =====
`
"""
AGT Users Service v1.0 - Django Settings
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "apps.users",
    "apps.roles",
    "apps.documents",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
}]

import dj_database_url
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
    )
}

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/1")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

def _read_key(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

AUTH_SERVICE_URL = config("AUTH_SERVICE_URL", default="")
AUTH_ADMIN_API_KEY = config("AUTH_ADMIN_API_KEY", default="")
AUTH_PUBLIC_KEY = _read_key(
    config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem"))
)

MEDIA_SERVICE_URL = config("MEDIA_SERVICE_URL", default="")
NOTIFICATION_SERVICE_URL = config("NOTIFICATION_SERVICE_URL", default="")

PERMISSION_CACHE_TTL = config("PERMISSION_CACHE_TTL", default=300, cast=int)
PROFILE_CACHE_TTL = config("PROFILE_CACHE_TTL", default=60, cast=int)
DEFAULT_HARD_DELETE_DELAY_DAYS = config("DEFAULT_HARD_DELETE_DELAY_DAYS", default=30, cast=int)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["apps.users.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "apps.users.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "apps.users.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "AGT Users Service API",
    "DESCRIPTION": "Service de gestion des utilisateurs : profils, RBAC dynamique, documents, metadonnees.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {"name": "Health", "description": "Etat du service"},
        {"name": "Profile", "description": "CRUD profil utilisateur"},
        {"name": "Sync", "description": "Synchronisation depuis Auth"},
        {"name": "Addresses", "description": "CRUD adresses"},
        {"name": "Roles", "description": "CRUD roles par plateforme"},
        {"name": "Permissions", "description": "CRUD permissions et verification"},
        {"name": "User Roles", "description": "Assignation roles aux utilisateurs"},
        {"name": "Documents", "description": "Documents KYC et workflow validation"},
        {"name": "Metadata", "description": "Metadonnees cle-valeur par plateforme"},
    ],
}

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
CORS_ALLOW_CREDENTIALS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\settings_test.py =====
`
"""Settings test - SQLite memoire, cache local, cle RSA generee."""
from config.settings import *  # noqa
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

AUTH_SERVICE_URL = ""
AUTH_ADMIN_API_KEY = "test-admin-key"
NOTIFICATION_SERVICE_URL = ""
MEDIA_SERVICE_URL = ""

LOGGING = {"version": 1, "disable_existing_loggers": True,
           "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.roles.urls")),
    path("api/v1/", include("apps.documents.urls")),

    # Swagger / OpenAPI 3.0
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-users\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\.env =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://wallet_user:wallet_password@db:5432/agt_wallet_db
REDIS_URL=redis://redis:6379/6
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\.env.example =====
`
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://wallet_user:wallet_password@db:5432/agt_wallet_db
REDIS_URL=redis://redis:6379/6
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\CDC_v1.0.md =====
`
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

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\docker-compose.yml =====
`
services:
  db:
    image: postgres:15-alpine
    container_name: agt_wallet_db
    restart: unless-stopped
    environment:
      POSTGRES_DB: agt_wallet_db
      POSTGRES_USER: wallet_user
      POSTGRES_PASSWORD: wallet_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5437:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U wallet_user -d agt_wallet_db"]
      interval: 10s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    container_name: agt_wallet_redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    ports:
      - "6384:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
  wallet:
    build:
      context: .
      target: production
    container_name: agt_wallet_service
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://wallet_user:wallet_password@db:5432/agt_wallet_db
      REDIS_URL: redis://redis:6379/6
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - ./keys:/app/keys:ro
    ports:
      - "7006:7006"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:7006/api/v1/wallet/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  wallet-dev:
    build:
      context: .
      target: builder
    container_name: agt_wallet_dev
    command: sh -c "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:7006"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://wallet_user:wallet_password@db:5432/agt_wallet_db
      REDIS_URL: redis://redis:6379/6
      DEBUG: "True"
      AUTH_SERVICE_PUBLIC_KEY_PATH: /app/keys/auth_public.pem
    volumes:
      - .:/app
      - ./keys:/app/keys:ro
    ports:
      - "7006:7006"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles:
      - dev
volumes:
  postgres_data:
  redis_data:

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\Dockerfile =====
`
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7006
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7006", "--workers", "4"]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\manage.py =====
`
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__ == "__main__": main()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\README.md =====
`
# AGT Wallet Service - v1.0

Ledger double-entry centralise. Wallets, holds, splits, cash-in/out.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
# Ouvrir Docker Desktop
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Documentation API
| URL | Description |
|-----|-------------|
| http://localhost:7006/api/v1/docs/ | Swagger UI |
| http://localhost:7006/api/v1/redoc/ | ReDoc |

## Tests
```bash
docker compose exec wallet python -m pytest -v
```

## Endpoints

### Accounts
- POST /wallet/accounts (creer wallet)
- GET /wallet/accounts/{id} (detail + solde disponible)
- GET /wallet/accounts/by-owner/{ownerId}
- POST /wallet/accounts/{id}/freeze | /unfreeze

### Ledger (double-entry)
- POST /wallet/credit
- POST /wallet/debit
- POST /wallet/transfer
- POST /wallet/split (partage commission multi-beneficiaire)
- GET /wallet/accounts/{id}/transactions (historique)

### Holds
- POST /wallet/holds (reservation)
- POST /wallet/holds/{id}/capture
- POST /wallet/holds/{id}/release

### Split Rules
- POST/GET /wallet/split-rules

### Admin
- GET /wallet/admin/stats
- POST /wallet/admin/audit-ledger (verification equilibre)
- POST /wallet/admin/adjustment (correctif avec justification)

Voir [CDC_v1.0.md](./CDC_v1.0.md)

Port : **7006**

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\requirements.txt =====
`
Django==5.0.4
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.4
PyJWT==2.8.0
cryptography==42.0.5
drf-spectacular==0.27.2
python-decouple==3.8
httpx==0.27.0
gunicorn==22.0.0
pytest==8.2.0
pytest-django==4.8.0
coverage==7.5.1

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\accounts\models.py =====
`
"""AGT Wallet Service v1.0 - Modeles. Double-entry ledger, append-only."""
import uuid
from django.db import models
from django.utils import timezone


class AccountType(models.TextChoices):
    USER = "user", "User"
    ORGANIZATION = "organization", "Organization"
    PLATFORM_SYSTEM = "platform_system", "Platform System"
    ESCROW = "escrow", "Escrow"
    EXTERNAL = "external", "External"


class AccountStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    FROZEN = "frozen", "Frozen"
    CLOSED = "closed", "Closed"


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    owner_type = models.CharField(max_length=20)  # user, organization, system
    owner_id = models.UUIDField(null=True, blank=True, db_index=True)
    currency = models.CharField(max_length=3, default="XAF")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    hold_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    label = models.CharField(max_length=100, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "accounts"
        ordering = ["-created_at"]

    @property
    def available_balance(self):
        return self.balance - self.hold_amount

    def is_frozen(self):
        return self.status == AccountStatus.FROZEN

    def can_debit(self, amount):
        if self.account_type == AccountType.EXTERNAL:
            return True  # External peut etre negatif
        return self.available_balance >= amount


class LedgerTransaction(models.Model):
    TX_TYPES = [
        ("cashin", "Cash In"), ("cashout", "Cash Out"), ("transfer", "Transfer"),
        ("split", "Split"), ("hold_capture", "Hold Capture"), ("hold_release", "Hold Release"),
        ("adjustment", "Adjustment"), ("reversal", "Reversal"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ledger_reference_id = models.CharField(max_length=30, unique=True)
    idempotency_key = models.UUIDField(unique=True)
    transaction_type = models.CharField(max_length=30, choices=TX_TYPES)
    platform_id = models.UUIDField()
    source = models.CharField(max_length=30)  # payment, platform, admin, cron
    source_reference_id = models.UUIDField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default="completed")  # completed, reversed
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ledger_transactions"
        ordering = ["-created_at"]

    @staticmethod
    def generate_reference():
        from django.utils.timezone import now
        year = now().year
        last = LedgerTransaction.objects.filter(ledger_reference_id__startswith=f"LTX-{year}").count()
        return f"LTX-{year}-{str(last + 1).zfill(6)}"


class LedgerEntry(models.Model):
    DIRECTION_CHOICES = [("debit", "Debit"), ("credit", "Credit")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(LedgerTransaction, on_delete=models.CASCADE, related_name="entries")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="entries")
    direction = models.CharField(max_length=6, choices=DIRECTION_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ledger_entries"
        ordering = ["created_at"]
        indexes = [models.Index(fields=["account", "created_at"])]


class HoldStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CAPTURED = "captured", "Captured"
    RELEASED = "released", "Released"
    EXPIRED = "expired", "Expired"


class Hold(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="holds")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=HoldStatus.choices, default=HoldStatus.PENDING)
    reason = models.CharField(max_length=50)
    reference_id = models.UUIDField(null=True, blank=True)
    idempotency_key = models.UUIDField(unique=True)
    expires_at = models.DateTimeField()
    captured_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "holds"
        ordering = ["-created_at"]


class CashoutRequest(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("processing", "Processing"), ("completed", "Completed"), ("failed", "Failed"), ("cancelled", "Cancelled")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cashout_requests")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    destination_provider = models.CharField(max_length=30)
    destination_details = models.JSONField()
    status = models.CharField(max_length=20, default="pending")
    hold = models.ForeignKey(Hold, on_delete=models.SET_NULL, null=True, blank=True)
    payment_tx_id = models.UUIDField(null=True, blank=True)
    idempotency_key = models.UUIDField(unique=True)
    failure_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cashout_requests"
        ordering = ["-created_at"]


class SplitRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField()
    name = models.CharField(max_length=100)
    rules = models.JSONField()  # [{"target": "seller", "percent": 85}, {"target": "platform", "percent": 15}]
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "split_rules"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\accounts\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\cashout\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\holds\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\service.py =====
`
"""AGT Wallet Service v1.0 - Ledger service. Double-entry bookkeeping. Append-only."""
import logging
from decimal import Decimal
from django.db import transaction as db_transaction
from django.utils import timezone
from apps.accounts.models import Account, LedgerTransaction, LedgerEntry, Hold, HoldStatus

logger = logging.getLogger(__name__)


class LedgerService:

    @classmethod
    def credit(cls, account_id, amount, currency, platform_id, source, source_reference_id, idempotency_key, description=None):
        return cls._single_entry("cashin", account_id, Decimal(str(amount)), currency, platform_id, source, source_reference_id, idempotency_key, description, direction="credit")

    @classmethod
    def debit(cls, account_id, amount, currency, platform_id, source, source_reference_id, idempotency_key, description=None):
        return cls._single_entry("cashout", account_id, Decimal(str(amount)), currency, platform_id, source, source_reference_id, idempotency_key, description, direction="debit")

    @classmethod
    def transfer(cls, from_account_id, to_account_id, amount, currency, platform_id, idempotency_key, description=None):
        existing = LedgerTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        amount = Decimal(str(amount))
        with db_transaction.atomic():
            from_acc = Account.objects.select_for_update().get(id=from_account_id)
            to_acc = Account.objects.select_for_update().get(id=to_account_id)

            if from_acc.is_frozen() or to_acc.is_frozen():
                return None, "account_frozen"
            if not from_acc.can_debit(amount):
                return None, "insufficient_balance"

            ltx = LedgerTransaction.objects.create(
                ledger_reference_id=LedgerTransaction.generate_reference(),
                idempotency_key=idempotency_key, transaction_type="transfer",
                platform_id=platform_id, source="platform", description=description,
            )

            from_acc.balance -= amount
            from_acc.save(update_fields=["balance", "updated_at"])
            LedgerEntry.objects.create(transaction=ltx, account=from_acc, direction="debit", amount=amount, balance_after=from_acc.balance)

            to_acc.balance += amount
            to_acc.save(update_fields=["balance", "updated_at"])
            LedgerEntry.objects.create(transaction=ltx, account=to_acc, direction="credit", amount=amount, balance_after=to_acc.balance)

        return ltx, None

    @classmethod
    def split(cls, source_account_id, amount, currency, platform_id, targets, idempotency_key, source_reference_id=None, description=None):
        existing = LedgerTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        amount = Decimal(str(amount))
        total_credit = sum(Decimal(str(t["amount"])) for t in targets)
        if total_credit != amount:
            return None, "split_unbalanced"

        with db_transaction.atomic():
            source_acc = Account.objects.select_for_update().get(id=source_account_id)
            if source_acc.is_frozen():
                return None, "account_frozen"
            if not source_acc.can_debit(amount):
                return None, "insufficient_balance"

            ltx = LedgerTransaction.objects.create(
                ledger_reference_id=LedgerTransaction.generate_reference(),
                idempotency_key=idempotency_key, transaction_type="split",
                platform_id=platform_id, source="platform",
                source_reference_id=source_reference_id, description=description,
            )

            source_acc.balance -= amount
            source_acc.save(update_fields=["balance", "updated_at"])
            LedgerEntry.objects.create(transaction=ltx, account=source_acc, direction="debit", amount=amount, balance_after=source_acc.balance)

            for t in targets:
                target_acc = Account.objects.select_for_update().get(id=t["account_id"])
                t_amount = Decimal(str(t["amount"]))
                target_acc.balance += t_amount
                target_acc.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=target_acc, direction="credit", amount=t_amount, balance_after=target_acc.balance)

        return ltx, None

    @classmethod
    def create_hold(cls, account_id, amount, reason, idempotency_key, expires_seconds=3600, reference_id=None):
        existing = Hold.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        amount = Decimal(str(amount))
        with db_transaction.atomic():
            acc = Account.objects.select_for_update().get(id=account_id)
            if acc.is_frozen():
                return None, "account_frozen"
            if not acc.can_debit(amount):
                return None, "insufficient_balance"

            acc.hold_amount += amount
            acc.save(update_fields=["hold_amount", "updated_at"])

            hold = Hold.objects.create(account=acc, amount=amount, reason=reason, reference_id=reference_id,
                                        idempotency_key=idempotency_key, expires_at=timezone.now() + timezone.timedelta(seconds=expires_seconds))
        return hold, None

    @classmethod
    def capture_hold(cls, hold_id, capture_amount=None):
        with db_transaction.atomic():
            try:
                hold = Hold.objects.select_for_update().get(id=hold_id, status=HoldStatus.PENDING)
            except Hold.DoesNotExist:
                return None, "hold_not_found"
            amount = Decimal(str(capture_amount)) if capture_amount else hold.amount
            acc = Account.objects.select_for_update().get(id=hold.account_id)
            hold.status = HoldStatus.CAPTURED
            hold.captured_amount = amount
            hold.resolved_at = timezone.now()
            hold.save(update_fields=["status", "captured_amount", "resolved_at"])
            acc.hold_amount -= hold.amount
            acc.balance -= amount
            acc.save(update_fields=["hold_amount", "balance", "updated_at"])
        return hold, None

    @classmethod
    def release_hold(cls, hold_id):
        with db_transaction.atomic():
            try:
                hold = Hold.objects.select_for_update().get(id=hold_id, status=HoldStatus.PENDING)
            except Hold.DoesNotExist:
                return None, "hold_not_found"
            acc = Account.objects.select_for_update().get(id=hold.account_id)
            acc.hold_amount -= hold.amount
            acc.save(update_fields=["hold_amount", "updated_at"])
            hold.status = HoldStatus.RELEASED
            hold.resolved_at = timezone.now()
            hold.save(update_fields=["status", "resolved_at"])
        return hold, None

    @classmethod
    def _single_entry(cls, tx_type, account_id, amount, currency, platform_id, source, source_reference_id, idempotency_key, description, direction):
        existing = LedgerTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        with db_transaction.atomic():
            acc = Account.objects.select_for_update().get(id=account_id)
            if acc.is_frozen():
                return None, "account_frozen"
            if direction == "debit" and not acc.can_debit(amount):
                return None, "insufficient_balance"

            external = Account.objects.filter(account_type="external", currency=currency).first()
            if not external:
                external = Account.objects.create(account_type="external", owner_type="system", currency=currency, label=f"External {currency}")

            ltx = LedgerTransaction.objects.create(
                ledger_reference_id=LedgerTransaction.generate_reference(),
                idempotency_key=idempotency_key, transaction_type=tx_type,
                platform_id=platform_id, source=source, source_reference_id=source_reference_id, description=description,
            )

            if direction == "credit":
                external.balance -= amount
                external.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=external, direction="debit", amount=amount, balance_after=external.balance)
                acc.balance += amount
                acc.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=acc, direction="credit", amount=amount, balance_after=acc.balance)
            else:
                acc.balance -= amount
                acc.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=acc, direction="debit", amount=amount, balance_after=acc.balance)
                external.balance += amount
                external.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=external, direction="credit", amount=amount, balance_after=external.balance)

        return ltx, None

    @classmethod
    def verify_integrity(cls):
        from django.db.models import Sum
        debits = LedgerEntry.objects.filter(direction="debit").aggregate(s=Sum("amount"))["s"] or 0
        credits = LedgerEntry.objects.filter(direction="credit").aggregate(s=Sum("amount"))["s"] or 0
        return {"balanced": debits == credits, "total_debits": float(debits), "total_credits": float(credits)}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\urls.py =====
`
from django.urls import path
from apps.ledger.views import (
    HealthCheckView, AccountCreateView, AccountDetailView, AccountByOwnerView,
    AccountFreezeView, AccountUnfreezeView, CreditView, DebitView, TransferView,
    SplitView, TransactionHistoryView, HoldCreateView, HoldCaptureView, HoldReleaseView,
    SplitRuleListCreateView, AdminStatsView, AdminAuditView, AdminAdjustmentView,
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
    path("wallet/holds", HoldCreateView.as_view()),
    path("wallet/holds/<uuid:hold_id>/capture", HoldCaptureView.as_view()),
    path("wallet/holds/<uuid:hold_id>/release", HoldReleaseView.as_view()),
    path("wallet/split-rules", SplitRuleListCreateView.as_view()),
    path("wallet/admin/stats", AdminStatsView.as_view()),
    path("wallet/admin/audit-ledger", AdminAuditView.as_view()),
    path("wallet/admin/adjustment", AdminAdjustmentView.as_view()),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\views.py =====
`
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
            owner_id=d.get("owner_id"), currency=d.get("currency", "XAF"), label=d.get("label"))
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
    @extend_schema(tags=["Ledger"], summary="Crediter un compte (double-entry)")
    def post(self, request):
        d = request.data
        ltx, err = LedgerService.credit(
            d.get("account_id"), d.get("amount"), d.get("currency", "XAF"),
            d.get("platform_id"), d.get("source", "payment"),
            d.get("source_reference_id"), d.get("idempotency_key"),
            d.get("description"), d.get("metadata"))
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
    @extend_schema(tags=["Ledger"], summary="Debiter un compte (double-entry)")
    def post(self, request):
        d = request.data
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
    @extend_schema(tags=["Ledger"], summary="Virement entre comptes")
    def post(self, request):
        d = request.data
        ltx, err = LedgerService.transfer(
            d.get("from_account_id"), d.get("to_account_id"), d.get("amount"),
            d.get("currency", "XAF"), d.get("platform_id"),
            d.get("idempotency_key"), d.get("description"))
        if err == "idempotent_hit":
            return Response({"transaction_id": str(ltx.id), "message": "Idempotent hit"})
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"transaction_id": str(ltx.id), "message": "Transfer completed"}, status=status.HTTP_201_CREATED)


class SplitView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Ledger"], summary="Split (partage commission)")
    def post(self, request):
        d = request.data
        ltx, err = LedgerService.split(
            d.get("source_account_id"), d.get("amount"), d.get("currency", "XAF"),
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
    @extend_schema(tags=["Holds"], summary="Creer un hold")
    def post(self, request):
        d = request.data
        hold, err = LedgerService.create_hold(
            d.get("account_id"), d.get("amount"), d.get("currency", "XAF"),
            d.get("reason"), d.get("source_reference_id"), d.get("ttl_seconds", 3600))
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"hold_id": str(hold.id), "amount": float(hold.amount),
                         "expires_at": hold.expires_at.isoformat()}, status=status.HTTP_201_CREATED)


class HoldCaptureView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Holds"], summary="Capturer un hold")
    def post(self, request, hold_id):
        hold, err = LedgerService.capture_hold(hold_id, request.data.get("platform_id", ""))
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
        return Response(LedgerService.audit_balance())


class AdminAdjustmentView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Admin"], summary="Ajustement correctif")
    def post(self, request):
        d = request.data
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

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\tests\test_all.py =====
`
"""AGT Wallet Service v1.0 - Tests. Double-entry ledger."""
import uuid
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import Account, LedgerEntry, LedgerTransaction, Hold
from apps.ledger.service import LedgerService


def make_account(account_type="user", currency="XAF", balance=0, **kw):
    return Account.objects.create(
        account_type=account_type, owner_type=kw.get("owner_type", "user"),
        owner_id=kw.get("owner_id", uuid.uuid4()), currency=currency,
        balance=Decimal(str(balance)), label=kw.get("label"))


class TestDoubleEntry(TestCase):
    def test_credit_creates_balanced_entries(self):
        acc = make_account(balance=0)
        ltx, err = LedgerService.credit(str(acc.id), 10000, "XAF", uuid.uuid4(), "payment")
        self.assertIsNone(err)
        entries = LedgerEntry.objects.filter(transaction=ltx)
        debits = sum(e.amount for e in entries if e.direction == "debit")
        credits = sum(e.amount for e in entries if e.direction == "credit")
        self.assertEqual(debits, credits)
        acc.refresh_from_db()
        self.assertEqual(acc.balance, Decimal("10000"))

    def test_debit_insufficient_balance(self):
        acc = make_account(balance=100)
        _, err = LedgerService.debit(str(acc.id), 500, "XAF", uuid.uuid4(), "platform")
        self.assertEqual(err, "insufficient_balance")

    def test_debit_success(self):
        acc = make_account(balance=10000)
        ltx, err = LedgerService.debit(str(acc.id), 3000, "XAF", uuid.uuid4(), "platform")
        self.assertIsNone(err)
        acc.refresh_from_db()
        self.assertEqual(acc.balance, Decimal("7000"))

    def test_transfer(self):
        a1 = make_account(balance=5000)
        a2 = make_account(balance=0)
        ltx, err = LedgerService.transfer(str(a1.id), str(a2.id), 2000, "XAF", uuid.uuid4())
        self.assertIsNone(err)
        a1.refresh_from_db()
        a2.refresh_from_db()
        self.assertEqual(a1.balance, Decimal("3000"))
        self.assertEqual(a2.balance, Decimal("2000"))

    def test_split_balanced(self):
        src = make_account(account_type="escrow", balance=10000)
        t1 = make_account(balance=0)
        t2 = make_account(balance=0)
        ltx, err = LedgerService.split(str(src.id), 10000, "XAF", uuid.uuid4(),
                                         [{"account_id": str(t1.id), "amount": 8500},
                                          {"account_id": str(t2.id), "amount": 1500}])
        self.assertIsNone(err)
        src.refresh_from_db()
        t1.refresh_from_db()
        t2.refresh_from_db()
        self.assertEqual(src.balance, Decimal("0"))
        self.assertEqual(t1.balance, Decimal("8500"))
        self.assertEqual(t2.balance, Decimal("1500"))

    def test_split_unbalanced_rejected(self):
        src = make_account(balance=10000)
        t1 = make_account()
        _, err = LedgerService.split(str(src.id), 10000, "XAF", uuid.uuid4(),
                                       [{"account_id": str(t1.id), "amount": 9000}])
        self.assertEqual(err, "split_unbalanced")

    def test_idempotency(self):
        acc = make_account()
        key = uuid.uuid4()
        LedgerService.credit(str(acc.id), 5000, "XAF", uuid.uuid4(), "payment", idempotency_key=key)
        _, err = LedgerService.credit(str(acc.id), 5000, "XAF", uuid.uuid4(), "payment", idempotency_key=key)
        self.assertEqual(err, "idempotent_hit")
        acc.refresh_from_db()
        self.assertEqual(acc.balance, Decimal("5000"))

    def test_frozen_account(self):
        acc = make_account(balance=10000)
        acc.status = "frozen"
        acc.save()
        _, err = LedgerService.credit(str(acc.id), 1000, "XAF", uuid.uuid4(), "payment")
        self.assertEqual(err, "account_frozen")

    def test_hold_and_available_balance(self):
        acc = make_account(balance=10000)
        hold, err = LedgerService.create_hold(str(acc.id), 3000, "XAF", "cashout")
        self.assertIsNone(err)
        acc.refresh_from_db()
        self.assertEqual(acc.hold_amount, Decimal("3000"))
        self.assertEqual(acc.available_balance, Decimal("7000"))

    def test_hold_capture(self):
        acc = make_account(balance=10000)
        hold, _ = LedgerService.create_hold(str(acc.id), 3000, "XAF")
        LedgerService.capture_hold(hold.id, uuid.uuid4())
        hold.refresh_from_db()
        acc.refresh_from_db()
        self.assertEqual(hold.status, "captured")
        self.assertEqual(acc.hold_amount, Decimal("0"))

    def test_hold_release(self):
        acc = make_account(balance=10000)
        hold, _ = LedgerService.create_hold(str(acc.id), 3000, "XAF")
        LedgerService.release_hold(hold.id)
        hold.refresh_from_db()
        acc.refresh_from_db()
        self.assertEqual(hold.status, "released")
        self.assertEqual(acc.hold_amount, Decimal("0"))
        self.assertEqual(acc.available_balance, Decimal("10000"))

    def test_audit_balanced(self):
        acc = make_account()
        LedgerService.credit(str(acc.id), 5000, "XAF", uuid.uuid4(), "payment")
        result = LedgerService.audit_balance()
        self.assertTrue(result["balanced"])
        self.assertEqual(result["anomalies"], 0)


class TestHealthEndpoint(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/wallet/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\apps\ledger\tests\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\common\authentication.py =====
`
import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.platform_id = p.get("platform_id")
        self.is_authenticated = True

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return None
        token = h.split(" ", 1)[1]
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached:
            return JWTPayload(cached), cached
        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try:
            payload = jwt.decode(token, pk, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload
    def authenticate_header(self, request):
        return "Bearer"

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\common\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\settings.py =====
`
from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost").split(",")
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.staticfiles", "rest_framework", "drf_spectacular", "corsheaders", "apps.accounts", "apps.ledger", "apps.holds"]
MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request"]}}]
import dj_database_url
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL", default="sqlite:///db.sqlite3"), conn_max_age=600)}
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/6")
CACHES = {"default": {"BACKEND": "django_redis.cache.RedisCache", "LOCATION": REDIS_URL, "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}}}
def _read_key(path):
    try:
        with open(path, "r") as f: return f.read()
    except FileNotFoundError: return ""
AUTH_PUBLIC_KEY = _read_key(config("AUTH_SERVICE_PUBLIC_KEY_PATH", default=str(BASE_DIR / "keys/auth_public.pem")))
REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ["common.authentication.JWTAuthentication"], "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"], "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"], "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", "UNAUTHENTICATED_USER": None}
SPECTACULAR_SETTINGS = {"TITLE": "AGT Wallet Service API", "VERSION": "1.0.0", "DESCRIPTION": "Ledger double-entry, wallets, holds, splits, cash-in/out.", "TAGS": [{"name": "Health"}, {"name": "Accounts"}, {"name": "Ledger"}, {"name": "Holds"}, {"name": "Split Rules"}, {"name": "Admin"}]}
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {"version": 1, "disable_existing_loggers": False, "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\settings_test.py =====
`
from config.settings import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
_k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
AUTH_PUBLIC_KEY = _k.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
LOGGING = {"version": 1, "disable_existing_loggers": True, "handlers": {"null": {"class": "logging.NullHandler"}}, "root": {"handlers": ["null"]}}

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\urls.py =====
`
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path("api/v1/", include("apps.ledger.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\wsgi.py =====
`
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\agt-wallet\config\__init__.py =====
`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GETTING_STARTED.md =====
`
# AGT Microservices - Getting Started

> Guide de demarrage rapide pour l'ecosysteme AGT. Ordre de lancement, premiers pas, et FAQ.

## Ordre de demarrage

Les services ont des dependances. Respectez cet ordre :

```
1. Auth      (port 7000) - en premier, genere les cles RSA
2. Users     (port 7001) - depend de la cle publique Auth
3. Notification (port 7002) - depend de la cle publique Auth
4. Subscription (port 7004) - depend de la cle publique Auth
5. Payment   (port 7005) - depend de la cle publique Auth
```

Les services 4+ (Payment, Wallet...) viendront ensuite.

## Demarrage complet (Windows)

```powershell
# 0. Ouvrir Docker Desktop et attendre qu'il soit pret

# 1. Auth
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 2. Users (nouveau terminal PowerShell)
cd agt-users
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 3. Notification (nouveau terminal PowerShell)
cd agt-notification
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 4. Subscription (nouveau terminal PowerShell)
cd agt-subscription
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Demarrage complet (Linux/macOS)

```bash
cd agt-auth && bash scripts/setup.sh && cd ..
cd agt-users && bash scripts/setup.sh && cd ..
cd agt-notification && bash scripts/setup.sh && cd ..
cd agt-subscription && bash scripts/setup.sh && cd ..
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 3. Notification (nouveau terminal PowerShell)
cd agt-notification
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Demarrage complet (Linux/macOS)

```bash
cd agt-auth && bash scripts/setup.sh && cd ..
cd agt-users && bash scripts/setup.sh && cd ..
cd agt-notification && bash scripts/setup.sh && cd ..
```

## Verification

```bash
curl http://localhost:7000/api/v1/auth/health
curl http://localhost:7001/api/v1/health
curl http://localhost:7002/api/v1/health
```

Les 3 doivent repondre `{"status": "healthy", ...}`.

## Premier flux complet

### 1. Creer une plateforme (sur Auth)

```bash
curl -X POST http://localhost:7000/api/v1/auth/platforms \
  -H "Content-Type: application/json" \
  -H "X-Admin-API-Key: change-me-admin-api-key-very-secret" \
  -d '{"name": "AGT Market", "slug": "agt-market", "allowed_auth_methods": ["email"]}'
```

Notez le `id` (UUID) et le `client_secret` retournes.

### 2. Inscrire un utilisateur

```bash
curl -X POST http://localhost:7000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "X-Platform-Id: <UUID-plateforme>" \
  -d '{"email": "test@agt.com", "password": "Test1234!", "method": "email"}'
```

Auth cree le compte ET provisionne automatiquement le profil dans Users.

### 3. Se connecter

```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@agt.com", "password": "Test1234!", "platform_id": "<UUID>"}'
```

Copiez l'`access_token` de la reponse.

### 4. Consulter le profil (sur Users)

```bash
curl http://localhost:7001/api/v1/users/by-auth/<auth-user-id> \
  -H "Authorization: Bearer <token>"
```

### 5. Envoyer une notification (sur Notification)

```bash
curl -X POST http://localhost:7002/api/v1/notifications/send \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<user-id>", "channels": ["in_app"], "template_name": "auth_verify_email", "variables": {"verification_url": "http://test.com", "expires_in_minutes": 60, "platform_name": "AGT Market"}}'
```

Note : creez d'abord le template (voir GUIDE_NOTIFICATION.md section 3.1).

### 6. Souscrire a un plan (sur Subscription)

```bash
# D'abord creer un plan (voir GUIDE_SUBSCRIPTION.md section 3.3)
# Puis souscrire
curl -X POST http://localhost:7004/api/v1/subscriptions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<UUID>", "subscriber_type": "user", "subscriber_id": "<auth-user-id>", "plan_id": "<plan-id>", "billing_cycle": "monthly"}'
```

## Ports

| Service | Port API | PostgreSQL | Redis | Autre |
|---------|----------|-----------|-------|-------|
| Auth | 7000 | 5432 | 6379 | - |
| Users | 7001 | 5433 | 6380 | - |
| Notification | 7002 | 5434 | 6381 | RabbitMQ 5672/15672 |
| Subscription | 7004 | 5435 | 6382 | - |
| Payment | 7005 | 5436 | 6383 | - |

## Documentation API (Swagger)

| Service | Swagger UI |
|---------|-----------|
| Auth | http://localhost:7000/api/v1/docs/ |
| Users | http://localhost:7001/api/v1/docs/ |
| Notification | http://localhost:7002/api/v1/docs/ |
| Subscription | http://localhost:7004/api/v1/docs/ |
| Subscription | http://localhost:7004/api/v1/docs/ |
| Payment | http://localhost:7005/api/v1/docs/ |

## FAQ

**Q: Docker dit "pipe not found" ou "unable to get image"**
A: Docker Desktop n'est pas demarre. Ouvrez-le et attendez l'icone verte.

**Q: "openssl n'est pas reconnu"**
A: Normal sur Windows. Le script genere les cles via Docker a la place.

**Q: Le service Users dit "AUTH_PUBLIC_KEY non configure"**
A: Copiez la cle publique : `copy ..\agt-auth\keys\public.pem keys\auth_public.pem`

**Q: L'inscription ne cree pas le profil Users**
A: Normal si Users n'est pas demarre. Auth log un warning mais l'inscription reussit. Demarrez Users et le provisioning fonctionnera pour les prochaines inscriptions.

**Q: Les emails/SMS ne s'envoient pas**
A: Normal en dev. Les providers (SendGrid, Twilio) ne sont pas configures. Les notifications sont creees en base avec status=failed. Utilisez le canal `in_app` pour tester.

**Q: Comment voir les logs ?**
A: `docker compose logs -f <service-name>` (auth, users, notification, celery-worker, etc.)

**Q: Comment tout arreter ?**
A: `docker compose down` dans chaque dossier service. Ajoutez `-v` pour supprimer les donnees.

## Guides detailles

- [GUIDE_AUTH.md](./GUIDE_AUTH.md) - Configuration et utilisation Auth
- [GUIDE_USERS.md](./GUIDE_USERS.md) - Configuration et utilisation Users
- [GUIDE_NOTIFICATION.md](./GUIDE_NOTIFICATION.md) - Configuration et utilisation Notification
- [GUIDE_SUBSCRIPTION.md](./GUIDE_SUBSCRIPTION.md) - Configuration et utilisation Subscription
- [GUIDE_SUBSCRIPTION.md](./GUIDE_SUBSCRIPTION.md) - Configuration et utilisation Subscription
- [GUIDE_PAYMENT.md](./GUIDE_PAYMENT.md) - Configuration et utilisation Payment (a venir)

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_AUTH.md =====
`
# Service Auth v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Auth de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop installe et **demarr** (icone verte dans la barre de taches)

### Lancement

**Windows :**
```powershell
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-auth
bash scripts/setup.sh
```

Le script fait tout automatiquement :
1. Cree le `.env` depuis `.env.example`
2. Genere les cles RSA (via OpenSSL ou via Docker si OpenSSL absent)
3. Build et demarre PostgreSQL + Redis + le service Auth
4. Execute les migrations
5. Verifie le health check

### Verification

```
curl http://localhost:7000/api/v1/auth/health
```

Reponse attendue :
```json
{"status": "healthy", "database": "ok", "redis": "ok", "version": "1.0.0"}
```

### Documentation API interactive

- **Swagger UI** : http://localhost:7000/api/v1/docs/
- **ReDoc** : http://localhost:7000/api/v1/redoc/

---

## 2. Premiere configuration

### 2.1 Creer une plateforme

Chaque application qui utilise Auth (AGT-Market, AGT-Bot, SALMA...) doit etre enregistree comme "plateforme". C'est le premier truc a faire.

```bash
curl -X POST http://localhost:7000/api/v1/auth/platforms \
  -H "Content-Type: application/json" \
  -H "X-Admin-API-Key: change-me-admin-api-key-very-secret" \
  -d '{
    "name": "AGT Market",
    "slug": "agt-market",
    "allowed_auth_methods": ["email", "phone", "google", "magic_link"],
    "allowed_redirect_urls": ["http://localhost:3000/callback"]
  }'
```

**Important** : la reponse contient un `client_secret` qui n'est affiche qu'une seule fois. Notez-le.

La reponse inclut aussi l'`id` de la plateforme (UUID). C'est le `X-Platform-Id` que vous passerez dans toutes les requetes.

### 2.2 Inscrire un utilisateur

```bash
curl -X POST http://localhost:7000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "X-Platform-Id: <UUID-plateforme>" \
  -d '{
    "email": "gabriel@agt.com",
    "password": "MonMotDePasse123!",
    "method": "email"
  }'
```

Note : la verification email est envoyee au Service Notification. En dev (Notification pas encore lance), l'inscription fonctionne mais l'email n'est pas envoye. L'utilisateur peut quand meme se connecter.

### 2.3 Se connecter

```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gabriel@agt.com",
    "password": "MonMotDePasse123!",
    "platform_id": "<UUID-plateforme>"
  }'
```

Reponse :
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

Le `refresh_token` est pose en cookie HttpOnly (pas visible dans la reponse JSON, mais present dans les headers Set-Cookie).

### 2.4 Utiliser le token

Tous les endpoints proteges des autres services acceptent ce token :

```bash
curl http://localhost:7001/api/v1/users \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."
```

---

## 3. Concepts cles

### JWT RS256
Auth signe les tokens avec une **cle privee** RSA. Les autres services (Users, Notification...) valident les tokens avec la **cle publique** â€” sans appeler Auth. C'est pour ca que chaque service a besoin de `keys/auth_public.pem`.

### Refresh Token Rotation
Le refresh token est un cookie HttpOnly. A chaque appel `POST /auth/refresh`, l'ancien est revoque et un nouveau est emis. Maximum 5 refresh tokens actifs par utilisateur (FIFO).

### Plateformes
Une plateforme = une application cliente. Chaque plateforme a ses propres methodes d'auth autorisees, ses redirect URLs, et son client_secret pour les tokens S2S.

### Admin API Key
Le header `X-Admin-API-Key` protege les endpoints d'administration (block, unblock, purge, gestion plateformes). La cle est definie dans `.env` (`ADMIN_API_KEY`).

---

## 4. Endpoints essentiels

| Action | Methode | Endpoint | Auth |
|--------|---------|----------|------|
| Creer plateforme | POST | `/auth/platforms` | Admin Key |
| Inscrire | POST | `/auth/register` | X-Platform-Id |
| Connecter | POST | `/auth/login` | - |
| Refresh token | POST | `/auth/refresh` | Cookie |
| Deconnecter | POST | `/auth/logout` | Bearer |
| Mon profil | GET | `/auth/me` | Bearer |
| Verifier token (S2S) | GET | `/auth/verify-token` | Bearer |

Liste complete : voir Swagger http://localhost:7000/api/v1/docs/

---

## 5. Tests

```bash
docker compose exec auth python -m pytest -v
```

26 tests couvrant : modeles, JWT, sessions, register, login, refresh, admin.

---

## 6. Arret et nettoyage

```bash
# Arreter
docker compose down

# Arreter et supprimer les donnees (reset complet)
docker compose down -v
```

---

## 7. Variables d'environnement cles

| Variable | Defaut | Description |
|----------|--------|-------------|
| `ADMIN_API_KEY` | change-me... | Cle admin pour endpoints admin |
| `JWT_ACCESS_TTL` | 900 | Duree access token (secondes) |
| `JWT_REFRESH_TTL` | 604800 | Duree refresh token (7 jours) |
| `BRUTE_FORCE_MAX` | 5 | Tentatives avant blocage |
| `BRUTE_FORCE_LOCKOUT` | 900 | Duree blocage (15 min) |
| `MAX_REFRESH_TOKENS` | 5 | Max tokens actifs par user |

Liste complete : voir `.env.example`

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_NOTIFICATION.md =====
`
# Service Notification v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Notification de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop **demarre**
- **Service Auth demarre en premier** (pour la cle publique RSA)

### Lancement

**Windows :**
```powershell
cd agt-notification
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-notification
bash scripts/setup.sh
```

> Ce service demarre 6 conteneurs : API, Celery Worker, Celery Beat, RabbitMQ, Redis, PostgreSQL. Le demarrage prend ~15 secondes.

### Verification

```
curl http://localhost:7002/api/v1/health
```

Reponse attendue :
```json
{"status": "healthy", "database": "ok", "redis": "ok", "broker": "ok", "version": "1.0.0"}
```

### URLs

| URL | Description | Credentials |
|-----|-------------|-------------|
| http://localhost:7002/api/v1/docs/ | Swagger UI | - |
| http://localhost:7002/api/v1/redoc/ | ReDoc | - |
| http://localhost:15672 | RabbitMQ Management | **guest / guest** |

---

## 2. Architecture du service

```
Client -> API Django (:7002) -> RabbitMQ -> Celery Worker (envoi async)
                                         -> Celery Beat (scheduled)
```

Le flux d'envoi :
1. Un service (Auth, Users...) appelle `POST /notifications/send`
2. L'API cree la notification en base (status=pending) et la place en queue RabbitMQ
3. Le Celery Worker consomme le message et envoie via le provider (SendGrid, Twilio, FCM...)
4. En cas d'echec : retry 3x backoff > autre provider > fallback inter-canal
5. Le statut est mis a jour : sent, delivered, ou failed

---

## 3. Premiere configuration

### 3.1 Creer les templates Auth

Le Service Auth envoie des emails/SMS via Notification. Il faut creer les templates **avant** de tester les fonctionnalites Auth qui envoient des notifications (register, forgot-password, magic-link).

Connectez-vous d'abord sur Auth pour obtenir un token, puis :

```bash
TOKEN="<votre-access-token>"

# Template verification email
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_verify_email",
    "channel": "email",
    "category": "transactional",
    "subject": "Verifiez votre email - {{ platform_name }}",
    "body": "<h1>Bienvenue</h1><p>Cliquez ici pour verifier : <a href=\"{{ verification_url }}\">Verifier</a></p><p>Expire dans {{ expires_in_minutes }} minutes.</p>"
  }'

# Template OTP SMS
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_otp_sms",
    "channel": "sms",
    "category": "security",
    "body": "Votre code AGT : {{ otp_code }}. Expire dans {{ expires_in_minutes }} min."
  }'

# Template reset password
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_reset_password",
    "channel": "email",
    "category": "security",
    "subject": "Reinitialisation mot de passe - {{ platform_name }}",
    "body": "<p>Cliquez pour reinitialiser : <a href=\"{{ reset_url }}\">Reset</a></p><p>Expire dans {{ expires_in_minutes }} minutes.</p>"
  }'

# Template magic link
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_magic_link",
    "channel": "email",
    "category": "transactional",
    "subject": "Connexion {{ platform_name }}",
    "body": "<p>Cliquez pour vous connecter : <a href=\"{{ magic_link_url }}\">Connexion</a></p><p>Expire dans {{ expires_in_minutes }} minutes.</p>"
  }'
```

### 3.2 Tester un envoi

```bash
curl -X POST http://localhost:7002/api/v1/notifications/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<uuid-user>",
    "channels": ["in_app"],
    "template_name": "auth_verify_email",
    "variables": {"verification_url": "http://example.com", "expires_in_minutes": 60, "platform_name": "AGT Market"}
  }'
```

Note : le canal `in_app` fonctionne toujours (pas de provider externe). Pour `email` et `sms`, configurez les API keys des providers dans `.env`.

### 3.3 Configurer les providers (optionnel en dev)

Dans `.env` :
```
# Email (SendGrid)
SENDGRID_API_KEY=SG.xxxxx

# SMS (Twilio)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_FROM_NUMBER=+1234567890

# Push (Firebase)
FCM_SERVER_KEY=xxxxx
```

Sans ces cles, les envois email/SMS echoueront (mais la notification sera cree en base avec status=failed, et un fallback in-app sera tente).

---

## 4. Utilisation courante

### Envoyer une notification

```bash
curl -X POST http://localhost:7002/api/v1/notifications/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<uuid>",
    "channels": ["email", "in_app"],
    "template_name": "order_confirmed",
    "variables": {"order_id": "ORD-123", "total": "15000 FCFA"},
    "category": "transactional",
    "priority": "high",
    "idempotency_key": "order-confirm-ORD-123"
  }'
```

### Notifications in-app

```bash
# Lister
curl http://localhost:7002/api/v1/users/<uid>/notifications \
  -H "Authorization: Bearer $TOKEN"

# Badge (non lues)
curl http://localhost:7002/api/v1/users/<uid>/notifications/unread-count \
  -H "Authorization: Bearer $TOKEN"

# Marquer comme lue
curl -X PUT http://localhost:7002/api/v1/users/<uid>/notifications/<nid>/read \
  -H "Authorization: Bearer $TOKEN"

# Tout marquer lu
curl -X PUT http://localhost:7002/api/v1/users/<uid>/notifications/read-all \
  -H "Authorization: Bearer $TOKEN"
```

### Campagnes (envoi en masse)

```bash
curl -X POST http://localhost:7002/api/v1/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Promo Noel 2026",
    "template_name": "promo_noel",
    "channel": "email",
    "user_ids": ["<uid1>", "<uid2>", "<uid3>"],
    "variables": {"discount": "20%"},
    "throttle_per_second": 5
  }'

# Suivre la progression
curl http://localhost:7002/api/v1/campaigns/<campaign-id>/progress \
  -H "Authorization: Bearer $TOKEN"
```

### Preferences utilisateur

```bash
# Lire
curl http://localhost:7002/api/v1/users/<uid>/notification-preferences \
  -H "Authorization: Bearer $TOKEN"

# Modifier
curl -X PUT http://localhost:7002/api/v1/users/<uid>/notification-preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channels": {"email": true, "sms": false, "push": true},
    "categories": {"marketing": false}
  }'
```

Note : `security` est toujours force a `true` (non modifiable).

---

## 5. RabbitMQ Management

Accessible sur http://localhost:15672

- **Username** : guest
- **Password** : guest

Vous y verrez les queues Celery, le nombre de messages en attente, et le debit d'envoi.

---

## 6. Templates : concepts

### Resolution
Quand vous envoyez avec `template_name: "order_confirmed"` :
1. Cherche un template avec ce nom **pour la plateforme du JWT**
2. Si pas trouve, cherche un template **global** (platform_id = null)
3. Si pas trouve, erreur 404

### Variables Jinja2
Les templates utilisent Jinja2. Toute syntaxe Jinja2 est supportee :
```
Bonjour {{ name }},
{% if discount %}Vous avez {{ discount }} de reduction !{% endif %}
```

### Versioning
Quand vous faites `PUT /templates/{id}`, l'ancienne version est archivee et une nouvelle est creee. On peut voir l'historique via `GET /templates/{id}/versions`.

### Preview
Avant d'envoyer, testez le rendu :
```bash
curl -X POST http://localhost:7002/api/v1/templates/<id>/preview \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"variables": {"name": "Gabriel", "discount": "20%"}}'
```

---

## 7. Tests

```bash
docker compose exec notification python -m pytest -v
```

15 tests couvrant : modeles, templates, envoi, idempotency, in-app.

---

## 8. Ports et credentials

| Ressource | URL | Credentials |
|-----------|-----|-------------|
| API Notification | http://localhost:7002 | JWT Bearer |
| Swagger | http://localhost:7002/api/v1/docs/ | - |
| RabbitMQ Management | http://localhost:15672 | guest / guest |
| PostgreSQL | localhost:5434 | notif_user / notif_password |
| Redis | localhost:6381 | - |

---

## 9. Logs et debug

```bash
# Logs API
docker compose logs -f notification

# Logs Worker (envois)
docker compose logs -f celery-worker

# Logs Scheduler
docker compose logs -f celery-beat
```

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_SUBSCRIPTION.md =====
`
# Service Subscription v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Subscription de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop **demarre**
- **Service Auth demarre en premier** (pour la cle publique RSA)

### Lancement

**Windows :**
```powershell
cd agt-subscription
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-subscription
bash scripts/setup.sh
```

### Verification

```
curl http://localhost:7004/api/v1/subscriptions/health
```

### URLs

| URL | Description |
|-----|-------------|
| http://localhost:7004/api/v1/docs/ | Swagger UI |
| http://localhost:7004/api/v1/redoc/ | ReDoc |

---

## 2. Concepts cles

### Plans
Un plan definit une offre : nom, prix (multi-cycle), quotas. Chaque plan est scope a une plateforme. Un plan peut etre gratuit (`is_free: true`), par defaut (`is_default: true`), ou payant.

### Quotas
Chaque plan definit N quotas avec une cle libre (ex: `max_bots`, `messages_per_month`, `storage_mb`). Deux politiques :
- **hard** : depassement interdit, acces bloque
- **overage** : depassement autorise, comptabilise pour facturation

### Subscriber
Abstrait : peut etre un `user` (B2C) ou une `organization` (B2B). Les quotas d'une organisation sont partages entre ses membres.

### Cycle de vie
```
pending_payment -> active -> [renouvellement OK] -> active
                     |
                     +-> cancelled (par l'abonne, actif jusqu'a fin cycle)
                     +-> [expiration] -> grace -> expired -> suspended

trial -> active (si paiement)
      -> [selon config] : downgrade_to_free | suspend | expire
```

### Prorata
Upgrade/downgrade en cours de cycle : credit restant ancien plan - cout restant nouveau plan = montant du.

---

## 3. Premiere configuration

### 3.1 Obtenir un token (via Auth)

```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@agt.com", "password": "MonPass123!", "platform_id": "<UUID>"}'
```

### 3.2 Configurer la plateforme

```bash
TOKEN="<votre-access-token>"

curl -X PUT http://localhost:7004/api/v1/subscriptions/config/<platform-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "default_trial_days": 14,
    "grace_period_days": 3,
    "post_trial_behavior": "suspend",
    "default_currency": "XAF",
    "allowed_cycles": ["monthly", "yearly"]
  }'
```

### 3.3 Creer un plan gratuit

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "<platform-id>",
    "name": "Free",
    "slug": "free",
    "is_free": true,
    "is_default": true,
    "tier_order": 0,
    "prices": [{"billing_cycle": "monthly", "price": 0, "currency": "XAF"}],
    "quotas": [
      {"quota_key": "max_bots", "limit_value": 1, "is_cyclical": false, "overage_policy": "hard"},
      {"quota_key": "messages_per_month", "limit_value": 100, "is_cyclical": true, "overage_policy": "hard"}
    ]
  }'
```

### 3.4 Creer un plan payant

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "<platform-id>",
    "name": "Pro",
    "slug": "pro",
    "tier_order": 2,
    "prices": [
      {"billing_cycle": "monthly", "price": 15000, "currency": "XAF"},
      {"billing_cycle": "yearly", "price": 150000, "currency": "XAF"}
    ],
    "quotas": [
      {"quota_key": "max_bots", "limit_value": 5, "is_cyclical": false, "overage_policy": "hard"},
      {"quota_key": "messages_per_month", "limit_value": 10000, "is_cyclical": true, "overage_policy": "overage", "overage_unit_price": 2}
    ]
  }'
```

### 3.5 Souscrire a un plan

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "<platform-id>",
    "subscriber_type": "user",
    "subscriber_id": "<user-auth-id>",
    "plan_id": "<plan-id>",
    "billing_cycle": "monthly",
    "with_trial": true
  }'
```

### 3.6 Activer apres paiement

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/<sub-id>/activate \
  -H "Authorization: Bearer $TOKEN"
```

---

## 4. Quotas (endpoints S2S critiques)

### Verifier (< 50ms, cache Redis)

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/quotas/check \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "subscriber_type": "user", "subscriber_id": "<uid>", "quota_key": "messages_per_month", "requested": 1}'
```

### Consommer

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/quotas/increment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "subscriber_type": "user", "subscriber_id": "<uid>", "quota_key": "messages_per_month", "amount": 1}'
```

### Reserve/Confirm/Release (atomique)

```bash
# 1. Reserver
curl -X POST .../quotas/reserve -d '{"platform_id": "...", "subscriber_type": "user", "subscriber_id": "...", "quota_key": "max_bots", "amount": 1}'

# 2a. Confirmer (si operation reussie)
curl -X POST .../quotas/confirm -d '{"reservation_id": "uuid"}'

# 2b. Liberer (si operation echouee)
curl -X POST .../quotas/release -d '{"reservation_id": "uuid"}'
```

---

## 5. Upgrade / Downgrade

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/<sub-id>/change-plan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"new_plan_id": "<premium-plan-id>", "billing_cycle": "monthly"}'
```

L'`amount_due` retourne doit etre transmis au Service Payment.

---

## 6. Organisations B2B

```bash
# Creer une organisation
curl -X POST http://localhost:7004/api/v1/organizations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "name": "ACME Corp", "owner_user_id": "<uid>"}'

# Ajouter un membre
curl -X POST http://localhost:7004/api/v1/organizations/<org-id>/members \
  -d '{"user_id": "<member-uid>"}'

# Souscrire pour l'org (quotas partages entre membres)
curl -X POST http://localhost:7004/api/v1/subscriptions \
  -d '{"platform_id": "...", "subscriber_type": "organization", "subscriber_id": "<org-id>", "plan_id": "...", "billing_cycle": "monthly"}'
```

---

## 7. Tests

```bash
docker compose exec subscription python -m pytest -v
```

---

## 8. Ports

| Ressource | URL |
|-----------|-----|
| API | http://localhost:7004 |
| Swagger | http://localhost:7004/api/v1/docs/ |
| ReDoc | http://localhost:7004/api/v1/redoc/ |
| PostgreSQL | localhost:5435 (sub_user / sub_password) |
| Redis | localhost:6382 |

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\docs\GUIDE_USERS.md =====
`
# Service Users v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Users de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop **demarre** (icone verte)
- **Service Auth demarre en premier** (pour la cle publique RSA)

### Lancement

**Windows :**
```powershell
cd agt-users
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-users
bash scripts/setup.sh
```

Le script copie automatiquement la cle publique depuis `../agt-auth/keys/public.pem`. Si le chemin est different, copiez manuellement :
```bash
cp <chemin-vers-auth>/keys/public.pem keys/auth_public.pem
```

### Verification

```
curl http://localhost:7001/api/v1/health
```

### Documentation API interactive

- **Swagger UI** : http://localhost:7001/api/v1/docs/
- **ReDoc** : http://localhost:7001/api/v1/redoc/

---

## 2. Comment ca marche

### Lien avec Auth
Le Service Users ne gere **pas** l'authentification. Il gere les **profils etendus** : nom, prenom, adresses, roles, permissions, documents KYC.

Le flux est :
1. L'utilisateur s'inscrit sur **Auth** (`POST /auth/register`)
2. Auth appelle automatiquement **Users** (`POST /users`) pour creer le profil
3. Le profil Users est lie a Auth par `auth_user_id`

### Convention d'identite
- `auth_user_id` = l'UUID de l'utilisateur dans Auth (= `sub` du JWT)
- `id` dans les endpoints Users = l'UUID interne du profil Users
- Pour passer de l'un a l'autre : `GET /users/by-auth/{auth_user_id}`

### Email et phone sont read-only
Les champs `email` et `phone` dans Users sont synchronises depuis Auth uniquement. L'endpoint `PUT /users/{id}` ne permet pas de les modifier. Seul Auth peut les changer via `POST /users/sync`.

---

## 3. Utilisation

### 3.1 Obtenir un token

Tout passe par Auth. Connectez-vous d'abord :
```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "gabriel@agt.com", "password": "MonMotDePasse123!", "platform_id": "<UUID>"}'
```

Recuperez l'`access_token` de la reponse.

### 3.2 Consulter un profil

```bash
# Par ID Users
curl http://localhost:7001/api/v1/users/<user-id> \
  -H "Authorization: Bearer <token>"

# Par auth_user_id (lookup)
curl http://localhost:7001/api/v1/users/by-auth/<auth-user-id> \
  -H "Authorization: Bearer <token>"
```

### 3.3 Modifier un profil

```bash
curl -X PUT http://localhost:7001/api/v1/users/<user-id> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Gabriel", "last_name": "Doe", "gender": "male"}'
```

Note : `email` et `phone` ne sont **pas** modifiables ici (read-only, source = Auth).

### 3.4 Gerer les adresses

```bash
# Ajouter
curl -X POST http://localhost:7001/api/v1/users/<id>/addresses \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type": "home", "street": "123 Rue Test", "city": "Yaounde", "country": "Cameroun"}'

# Lister
curl http://localhost:7001/api/v1/users/<id>/addresses \
  -H "Authorization: Bearer <token>"
```

### 3.5 RBAC : Roles et Permissions

Le RBAC est **100% dynamique** â€” aucun role ou permission n'est hardcode.

```bash
# 1. Creer un role pour une plateforme
curl -X POST http://localhost:7001/api/v1/platforms/<platform-id>/roles \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "vendeur", "description": "Vendeur sur la marketplace"}'

# 2. Creer une permission
curl -X POST http://localhost:7001/api/v1/platforms/<platform-id>/permissions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "create_product", "description": "Peut creer un produit"}'

# 3. Attacher la permission au role
curl -X POST http://localhost:7001/api/v1/platforms/<platform-id>/roles/<role-id>/permissions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"permission_id": "<perm-id>"}'

# 4. Assigner le role a un utilisateur
curl -X POST http://localhost:7001/api/v1/users/<user-id>/roles \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"role_id": "<role-id>"}'

# 5. Verifier une permission (cache Redis, < 200ms)
curl "http://localhost:7001/api/v1/users/<user-id>/permissions/check?platform_id=<pid>&permission=create_product" \
  -H "Authorization: Bearer <token>"
```

Reponse :
```json
{"user_id": "...", "platform_id": "...", "permission": "create_product", "granted": true, "via_role": "vendeur"}
```

### 3.6 Documents KYC

```bash
# Attacher un document
curl -X POST http://localhost:7001/api/v1/users/<id>/documents \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "doc_type": "identity_card", "media_id": "<uuid-du-fichier>"}'

# Valider un document (admin)
curl -X PUT http://localhost:7001/api/v1/users/<id>/documents/<doc-id>/status \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "validated", "comment": "Document conforme"}'
```

---

## 4. Modele de suppression

3 niveaux progressifs :

| Action | Endpoint | Effet |
|--------|----------|-------|
| Quitter une plateforme | `DELETE /users/{id}/platforms/{pid}` | Retire roles + metadata + archive docs. Profil intact. |
| Soft delete global | `DELETE /users/{id}` | Status=deleted, Auth desactive, hard_delete planifie (30j) |
| Hard delete RGPD | `DELETE /users/{id}/permanent` | Purge Auth + Users. Irreversible. |

---

## 5. Tests

```bash
docker compose exec users python -m pytest -v
```

17 tests couvrant : modeles, CRUD, sync, by-auth, leave-platform, RBAC.

---

## 6. Ports et credentials

| Ressource | URL |
|-----------|-----|
| API Users | http://localhost:7001 |
| Swagger | http://localhost:7001/api/v1/docs/ |
| PostgreSQL | localhost:5433 (users_user / users_password) |
| Redis | localhost:6380 |

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\next\prompt_fisrt_task.md =====
`
Nous commenÃ§ons maintenant la tÃ¢che 1 : prÃ©parer les simulateurs des services restants.

Travaille uniquement sur cette tÃ¢che.

Je veux que tu suives exactement cette mÃ©thode :

1. analyse de lâ€™existant
2. conception fonctionnelle
3. conception technique
4. mise en place / implÃ©mentation
5. tests

Pour lâ€™instant, fais seulement :

* lâ€™analyse de lâ€™existant
* puis la conception fonctionnelle

Ne code rien encore.
Sois concret et respecte strictement lâ€™architecture actuelle.

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\next\prompt_initialisation.md =====
`
Tu es mon pair-programmer principal pour AG Technologies.

Tu mâ€™accompagnes dans la mise en place de mon architecture microservices et de mon backend template, Ã©tape par Ã©tape, avec rigueur et discipline.

CONTEXTE

* Mon architecture est dÃ©jÃ  largement cadrÃ©e
* 8 services sur 11 sont dÃ©jÃ  faits en version 1.0
* Les versions sont maintenant correctement alignÃ©es
* Jâ€™ai les CDC, le code existant et une mini documentation
* Je vais te fournir tout ce contexte
* Nous allons travailler une seule tÃ¢che Ã  la fois

RÃ”LE
Tu es mon guide technique et mon pair-programmer fidÃ¨le.
Tu ne dois faire que ce que je demande, uniquement dans le pÃ©rimÃ¨tre demandÃ©.

RÃˆGLES ABSOLUES

* Tu travailles une tÃ¢che Ã  la fois
* Tu nâ€™anticipes jamais la tÃ¢che suivante sans mon signal
* Tu ne proposes pas de refonte globale si je demande une tÃ¢che locale
* Tu respectes strictement lâ€™architecture actuelle
* Tu respectes les conventions dÃ©jÃ  en place
* Tu privilÃ©gies la cohÃ©rence avec lâ€™existant
* Tu produis un code modulaire, lisible, commentÃ©, testable et scalable
* Tu ne gÃ©nÃ¨res pas du code avant dâ€™avoir analysÃ© lâ€™existant et clarifiÃ© la conception
* Tu mâ€™aides Ã  avancer pas Ã  pas

MÃ‰THODE DE TRAVAIL OBLIGATOIRE
Pour chaque tÃ¢che, tu suis exactement cet ordre :

1. Analyse de lâ€™existant

* ce qui existe dÃ©jÃ 
* ce quâ€™il faut rÃ©utiliser
* ce quâ€™il faut Ã©viter de casser

2. Conception fonctionnelle

* que va-t-on faire
* pourquoi
* quels choix mÃ©tier sont les bons

3. Conception technique

* ce qui sera fait techniquement
* fichiers concernÃ©s
* structure attendue
* dÃ©pendances Ã©ventuelles

4. Mise en place / implÃ©mentation

* gÃ©nÃ©ration du code demandÃ©
* uniquement dans le pÃ©rimÃ¨tre validÃ©

5. Tests

* tests Ã  prÃ©voir
* vÃ©rifications locales
* points de contrÃ´le

STYLE DE RÃ‰PONSE

* sois structurÃ©
* sois concret
* sois concis mais prÃ©cis
* Ã©vite les longs discours thÃ©oriques
* quand tu proposes du code, il doit Ãªtre exploitable directement
* quand une hypothÃ¨se est nÃ©cessaire, indique-la clairement

RÃˆGLE FINALE
Tu es mon pair-programmer, pas un agent autonome.
Tu avances avec moi, Ã  mon rythme, Ã©tape par Ã©tape.

`
===== FILE END =====

===== FILE START: C:\Users\hp\Documents\gabriel\AGT-SERVICES\next\prompt_todo.md =====
`
Nous allons travailler ensemble sur les prochaines Ã©tapes de mon architecture AG Technologies.

Contexte :

* 8 services sur 11 sont dÃ©jÃ  faits en 1.0
* lâ€™architecture actuelle est alignÃ©e correctement
* jâ€™ai les CDC, le code existant et une mini documentation
* les 2 prochaines prioritÃ©s sont :

  1. coder les simulateurs des services restants en respectant lâ€™architecture actuelle
  2. implÃ©menter le backend template

Je veux dâ€™abord que tu mâ€™aides Ã  produire un fichier todo.md simple, souple et exploitable.

Contraintes pour cette todo :

* elle doit rester simple
* elle ne doit pas Ãªtre trop dÃ©taillÃ©e
* elle doit montrer les grandes lignes du travail
* elle doit inclure notre dÃ©marche de travail pour chaque tÃ¢che :

  * analyse de lâ€™existant
  * conception fonctionnelle
  * conception technique
  * mise en place / implÃ©mentation
  * tests

Je veux que tu me proposes le contenu complet du fichier todo.md en markdown, prÃªt Ã  copier.
Ne code rien dâ€™autre pour lâ€™instant.


---
# Exemple de todo qui peut em plaire 

# TODO â€” AGT Microservices Suite

## Objectif gÃ©nÃ©ral
Avancer proprement sur les prochaines Ã©tapes de lâ€™architecture AG Technologies en travaillant une tÃ¢che Ã  la fois, avec une dÃ©marche rigoureuse et rÃ©utilisable.

## MÃ©thode de travail
Pour chaque tÃ¢che :
- [ ] Analyse de lâ€™existant
- [ ] Conception fonctionnelle
- [ ] Conception technique
- [ ] Mise en place / implÃ©mentation
- [ ] Tests

---

## 1. PrÃ©parer les simulateurs des services restants
- [ ] Identifier prÃ©cisÃ©ment les services restants Ã  simuler
- [ ] DÃ©finir le rÃ´le de chaque simulateur dans lâ€™architecture actuelle
- [ ] Concevoir le comportement fonctionnel minimal attendu
- [ ] Concevoir la structure technique et les fichiers concernÃ©s
- [ ] ImplÃ©menter les simulateurs
- [ ] Tester localement les simulateurs

## 2. Mettre en place le backend template
- [ ] Analyser lâ€™architecture actuelle pour en extraire les briques communes
- [ ] DÃ©finir le pÃ©rimÃ¨tre fonctionnel du backend template
- [ ] DÃ©finir la structure technique du template
- [ ] ImplÃ©menter le backend template
- [ ] Ajouter les tests de base
- [ ] Valider le template en local

## 3. PrÃ©parer le terrain pour AGT-Bot
- [ ] Identifier ce que le backend template doit couvrir pour AGT-Bot
- [ ] VÃ©rifier les dÃ©pendances nÃ©cessaires
- [ ] PrÃ©parer lâ€™intÃ©gration future avec le dashboard de gÃ©nÃ©ration

## 4. Documentation progressive
- [ ] Mettre Ã  jour la documentation au fur et Ã  mesure
- [ ] Garder une trace claire des choix fonctionnels et techniques
- [ ] Documenter les commandes et les Ã©tapes de test local
`
===== FILE END =====

## SUMMARY
- Total files: 261

