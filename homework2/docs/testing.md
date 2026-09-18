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
