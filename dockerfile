
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
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt



FROM python:3.11-slim

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


RUN python manage.py collectstatic --noinput \
    && chown -R appuser:appuser staticfiles/


USER appuser

EXPOSE 8000


CMD ["gunicorn", "projet_app_immo.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "3", \
    "--timeout", "120", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]