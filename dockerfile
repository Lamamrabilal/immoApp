# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only what Django actually needs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN useradd --create-home appuser
USER appuser

# Copy project files
COPY --chown=appuser:appuser . .

# Expose Django's port
EXPOSE 8000

# Start Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]