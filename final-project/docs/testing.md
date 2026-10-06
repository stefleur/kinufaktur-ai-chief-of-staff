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

The revised GitHub Actions CI runs `uv run pytest -q`, frontend `npm ci`,
`npm run test:ci`, and `npm run build` on Node 22. The Pages workflow calls this
CI through `workflow_call` and requires successful checks before publication.
The current feature branch has not been pushed, so its commits have not run on
GitHub Actions.

For a manual demo, create/edit/move a synthetic task, reload to confirm
persistence, delete it, and reload to confirm removal. Production verification
is described in [deployment.md](deployment.md).

On 2026-10-06, the existing Compose stack built successfully and all three
services were healthy. Local frontend `/` and backend `/tasks` returned HTTP 200.
One uniquely named synthetic local task was created (201) and returned by the
list endpoint. After `docker compose -f final-project/docker-compose.yml restart
backend frontend`, its exact record survived in the list (200). Cleanup deleted
only that task (200), followed by its GET returning 404. `down` stopped the stack;
`ps -a` was empty and the named PostgreSQL volume remained. No runtime fix was
needed. This verifies local API restart persistence; browser CRUD and production
Neon persistence were not tested.

The backend Actions job is prepared with `needs: checks` and defaults to disabled
until the owner supplies its secrets and opt-in variable. Full backend gating
still requires the external provider cutover in [deployment.md](deployment.md).
The revised workflows have not run remotely. The clean-clone audit is recorded
in `docs/ai-development-workflow.md`.

Final regression after backend gate preparation: `npm run test:ci` passed all 9
frontend tests, `npm run build` passed (Vite 7.3.6), and `uv run pytest -q` passed
all 13 backend tests with two existing dependency deprecation warnings. Workflow
YAML parsed and both deploy jobs require `checks`; shell syntax passed. Running
the extracted backend deployment step without either credential exited 1 before
invoking the CLI. `git diff --check` passed. At that point in the Batch 3 work,
the changes remained uncommitted.

## Agent Extension Pack and security checks

From the repository root, install the isolated MCP environment and run the MCP
protocol and staged-path guardrail tests:

```bash
uv sync --project final-project/mcp-server --locked --group dev
uv run --project final-project/mcp-server --locked pytest -q \
    final-project/mcp-server/tests final-project/agent-hooks/tests
```

The deterministic scan runner requires Gitleaks 8.30.1 and Bandit 1.9.4:

```bash
bash final-project/security/run-scans.sh
```

For a manual local CRUD check, start Compose as described in `deployment.md`,
open `http://localhost:5173/`, create a synthetic task, edit it, change its
status, reload to confirm persistence, delete it, and reload to confirm removal.
Stop services without `down -v` so the named database volume is retained.
