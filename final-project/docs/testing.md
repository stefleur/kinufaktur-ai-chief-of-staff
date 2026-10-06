# KinuFlow testing

All commands start from the repository root unless a directory is specified.
Use synthetic fixtures only. Tests do not call production services.

## Backend API tests

`backend/tests/test_tasks.py` exercises CRUD, validation, missing tasks, and CORS
through FastAPI TestClient with an overridden database dependency and isolated
in-memory SQLite. These are API tests, not pure unit tests: they also exercise
SQLAlchemy data access.

```bash
cd final-project/backend
uv sync --locked --group dev
uv run pytest -q -m "not integration"
```

## Backend integration tests

`backend/tests/integration/test_integration_tasks.py` covers create, list, read,
edit, status change, and delete across requests. It uses real application wiring
and SQLAlchemy without overriding `get_db`. A fixture temporarily patches the
module-level engine/session factory and restores them afterward. Tables are
removed and the engine disposed even if an assertion fails.

```bash
# From final-project/backend:
uv run pytest -q -m integration
uv run pytest -q
```

The `integration` marker is registered in `backend/pyproject.toml`. The lifecycle
uses in-process HTTP handling and SQLite; it does not claim PostgreSQL, browser,
external-network, or deployed-service integration coverage.

## Frontend core tests

Vitest runs React Testing Library tests in jsdom. API modules/fetch are mocked;
there are no browser downloads, snapshots, or coverage thresholds.

- `src/App.test.jsx`: column rendering, loading errors, successful status moves,
  and restoration after a rejected optimistic move.
- `src/components/TaskForm.test.jsx`: required fields and normalized submission.
- `src/api/tasksApi.test.js`: successful JSON, backend errors, and network errors.

Use Node compatible with Vite 7 (20.19+ or 22.12+).

```bash
cd final-project/frontend
npm ci
npm run test:ci
npm run build
```

`npm test` runs the interactive watch mode. `npm run test:ci` runs once and exits
nonzero on failure. Setup cleans rendered DOM and restores mocks between tests.

## CI status and manual checks

The existing GitHub Actions CI runs `uv run pytest -q` and the frontend build.
The frontend test command is ready for CI, but adding it and fixing CI's Node 18
configuration are Batch 3 work. Batches 1/2 do not change CI or deployment.

For a manual demo, create/edit/move a synthetic task, reload to confirm
persistence, delete it, and reload to confirm removal. Production verification
is described in [deployment.md](deployment.md). Docker checks, deployment
proof, gating, and a final clean-clone audit are deferred to later batches.
