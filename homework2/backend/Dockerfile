FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1

FROM base as builder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./app ./app
COPY pyproject.toml ./pyproject.toml

# Install build-time dependencies (wheel, etc.)
RUN python -m pip install --upgrade pip setuptools wheel

FROM base
WORKDIR /app
COPY ./app ./app
COPY pyproject.toml ./pyproject.toml

# Install runtime dependencies in the final image so console scripts
# like `uvicorn` are available in PATH.
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir fastapi uvicorn[standard] sqlalchemy psycopg[binary]

ENV KINUFLOW_DATABASE_URL="sqlite:///./kinuflow.db"

EXPOSE 8000

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Use curl for a simple HTTP healthcheck.
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD curl -f http://127.0.0.1:${PORT:-8000}/tasks || exit 1

# Use the PORT environment variable when provided by the hosting platform
# (Render sets `PORT`). Fall back to 8000 for local development and
# Docker Compose.
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
