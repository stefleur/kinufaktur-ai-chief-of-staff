# KinuFlow backend

This directory contains the FastAPI backend for KinuFlow. It currently uses a
replaceable in-memory task store; no database is configured.

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
