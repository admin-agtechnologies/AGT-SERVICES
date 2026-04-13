# --------------------
# Builder
# --------------------
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------
# Production
# --------------------
FROM python:3.11-slim AS production
WORKDIR /app

# ---- FIX: Installer curl pour le health check Docker ----
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
# ---------------------------------------------------------

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE 7000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7000", "--workers", "4"]