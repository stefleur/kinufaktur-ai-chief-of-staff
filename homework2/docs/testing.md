Backend testing
===============

This document describes the existing backend test suite and the new integration tests.

Overview of existing backend tests
---------------------------------
- Location: [homework2/backend/tests](homework2/backend/tests)
- Purpose: Fast unit-style tests for the FastAPI application using `TestClient` and an in-memory SQLite database. These tests override the app's `get_db` dependency to provide a session bound to an in-memory engine, keeping tests isolated and fast.
- What they verify: request/response behavior, validation handling, CORS headers, and data-access logic through the `SqlAlchemyTaskStore` while using an in-memory DB via dependency override.

New integration tests
---------------------
- Location: [homework2/backend/tests/integration](homework2/backend/tests/integration)
- Purpose: Exercise the real FastAPI application and the real SQLAlchemy persistence layer without overriding the `get_db` dependency. The tests replace the module-level `database.engine` and `database.SessionLocal` with a dedicated test engine so the application uses a real DB backend during the test run.
- What they verify: the full task lifecycle end-to-end over HTTP (create, list, get, update, change status, delete) and that changes persist across requests.

How the integration tests work
-----------------------------
- The tests create a dedicated in-memory SQLite engine using `StaticPool` so the database connection can be shared across threads (the app runs in a different thread when using `TestClient`).
- The test reassigns `app.database.engine` and `app.database.SessionLocal` to point at the test engine, then calls `create_app(initialize_database=True)` so tables are created against the test database.
- No persistence layer is mocked; the store implementation `SqlAlchemyTaskStore` runs against the test database.

Running tests
-------------
Run integration tests only (from repo root):

```bash
cd agent1/homework2/backend
pytest -q tests/integration
```

Run all backend tests (unit + integration):

```bash
cd agent1/homework2/backend
pytest -q
```

What each level verifies
------------------------
- Unit-style backend tests (`tests/`): verify API semantics, validations, and handler-level behavior using a dependency-overridden DB session. Fast and suitable for CI.
- Integration tests (`tests/integration/`): verify the real application wiring, dependency resolution, and SQLAlchemy-backed persistence end-to-end via HTTP. Slightly heavier but still fast due to SQLite in-memory usage.

Notes and recommendations
-------------------------
- The integration tests intentionally avoid network or containerized DBs to keep CI fast. If you later add Postgres or other DB-backed integration tests, isolate them behind pytest markers and CI configuration.
- Keep tests small and deterministic; use `StaticPool` for in-memory SQLite when the FastAPI app runs in a different thread.

CI
--
The repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` which runs on pushes and pull requests to `main`.

What CI checks
- Backend non-integration tests: installs Python dependencies and runs `uv run pytest -m "not integration"` (fast unit-style checks).
- Backend integration tests: installs Python dependencies and runs `uv run pytest -m integration` (isolated, deterministic integration tests using in-memory SQLite).
- Frontend verification: runs `npm ci` and `npm run build`. If a `lint` npm script exists it will be invoked.
- Container verification: builds the backend and frontend Docker images and validates the `docker-compose.yml` with `docker compose config`.

When CI runs
- On `push` to `main` and on `pull_request` targeting `main`.

Corresponding commands (local equivalents)
- Backend non-integration tests:

```bash
cd agent1/homework2/backend
uv run pytest -m "not integration"
```

- Backend integration tests:

```bash
cd agent1/homework2/backend
uv run pytest -m integration
```

- Frontend verification:

```bash
cd agent1/homework2/frontend
npm ci
npm run build
```

- Container verification (local equivalent):

```bash
cd agent1/homework2
docker build -f backend/Dockerfile -t ci/homework2-backend:latest backend
docker build -f frontend/Dockerfile -t ci/homework2-frontend:latest frontend
docker compose config
```

Why CI must stop on required failures
- The workflow treats all checks as required; if unit tests, integration tests, build, or container verification fail, the change cannot be merged. This prevents regressions and ensures the build is reproducible in the same way CI runs it.
