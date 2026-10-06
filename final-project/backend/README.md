# KinuFlow backend

This directory contains the FastAPI backend for KinuFlow. Persistence is kept
behind a SQLAlchemy data-access layer.

By default, local data is stored in `kinuflow.db` inside this directory. To use
another SQLAlchemy-compatible database URL, set `KINUFLOW_DATABASE_URL` before
starting the server:

```bash
export KINUFLOW_DATABASE_URL="sqlite:///./kinuflow.db"
```

The required tables are created when the application starts.

## Install

```bash
uv sync
```

## Run the tests

```bash
uv run pytest
```

## Start the development server

```bash
uv run uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000` and its interactive Swagger UI
at `http://localhost:8000/docs`.
