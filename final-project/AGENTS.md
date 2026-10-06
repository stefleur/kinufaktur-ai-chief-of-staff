# KinuFlow project instructions

## Boundaries and context

KinuFlow is the AI Dev Tools Zoomcamp 2026 Final Project and lives in `final-project/`.
Read `docs/final-project-rubric.md` and `product-spec.md` before changes.
`openapi.yaml` is the canonical API contract; keep frontend needs,
backend responses, and validation aligned with it.

Preserve the root historical Django application, production URLs, database
schema, and working task CRUD. Keep one canonical implementation here.
Keep changes small and limited to the authorized batch. Do not commit, push,
merge, or deploy without authorization.

## Implementation

- React/Vite frontend: centralize HTTP calls in `frontend/src/api/tasksApi.js`.
- FastAPI/Pydantic backend: keep endpoints structured and validated.
- SQLAlchemy persistence: retain the separate store and SQLite/PostgreSQL support.
- Use uv and the existing Python lockfile; lock frontend dependencies with npm.
- Use synthetic/demo data only; never expose secrets in code, prompts, logs,
  documentation, or test results. Do not read production secrets for routine work.

Excluded scope: runtime LLM features, accounts/authentication, migrations,
PostgreSQL test infrastructure, Playwright/E2E, new cloud services, microservices,
workers/queues, Redis, Kafka, Kubernetes, and observability platforms.

Protected areas: historical Django code, credentials/environment files,
production provider settings, and `.github/workflows/` or Docker configuration
unless explicitly authorized. Relocation may correct repository paths only; Docker fixes, CI/CD redesign,
and provider changes remain Batch 3 work. Human review is required before
subsequent work and any commit, push, or deployment authorization.

## Verification

From `backend/`:

```bash
uv sync --locked --group dev
uv run pytest -q -m "not integration"
uv run pytest -q -m integration
uv run pytest -q
```

From `frontend/` (Node 20.19+ or 22.12+ compatible with locked Vite 7):

```bash
npm ci
npm run test:ci
npm run build
```

From repository root: `git diff --check`. See `docs/testing.md` for test levels.
Record actual checks and corrections in `docs/ai-development-workflow.md`.
Human approval of scope is not evidence of human review of an implementation;
label pending review accurately.
