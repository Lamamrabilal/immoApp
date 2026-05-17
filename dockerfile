
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    cmake \
    libpq-dev \
    libcairo2-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt



FROM python:3.11-slim AS production

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libcairo2 \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /install /usr/local


RUN useradd --create-home appuser


COPY --chown=appuser:appuser . .

# Ajouter une SECRET_KEY fictive juste pour le collectstatic
RUN SECRET_KEY=dummy-build-key \
    DJANGO_DATABASE_URL=postgresql://dummy:dummy@localhost/dummy \
    python manage.py collectstatic --noinput


USER appuser

EXPOSE 8000

# Healthcheck intégré
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "projet_app_immo.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "3", \
    "--timeout", "120", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]