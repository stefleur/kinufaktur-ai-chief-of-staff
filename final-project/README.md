# KinuFlow — AI Dev Tools Zoomcamp 2026 Final Project

KinuFlow helps the Kinufaktur operator turn incoming business requests into
visible, actionable work. The Kanban board supports viewing, creating, editing,
moving, and deleting tasks with title, description, category, and priority.
Saved changes persist after reload. Use synthetic/demo data only; AI assists
development and the application does not call an LLM.

## Architecture and technologies

- **Frontend:** React/Vite; HTTP calls centralized in `frontend/src/api/tasksApi.js`.
- **Backend:** FastAPI/Pydantic implementing the [OpenAPI contract](openapi.yaml).
- **Database:** SQLAlchemy data-access layer; SQLite for local development/tests,
  PostgreSQL for Docker Compose and Neon production.
- **Containers:** frontend nginx, backend FastAPI, and PostgreSQL in
  [docker-compose.yml](docker-compose.yml).
- **CI/CD:** repository-level [CI](../.github/workflows/ci.yml) runs backend tests
  and frontend tests/build. The separate [deployment workflow](../.github/workflows/deploy.yml)
  publishes GitHub Pages; FastAPI Cloud's GitHub integration deploys the backend.
  Pages calls the same verification before publishing. Backend deployment remains
  external and independently triggered. A backend Actions job is prepared but
  disabled by default; see the deployment guide for the exact owner cutover.

```text
GitHub Pages (React) -> FastAPI Cloud (API) -> Neon PostgreSQL
```

## Run locally

From the repository root, in separate terminals (uv/Python 3.11+ and Node
compatible with Vite 7: 20.19+ or 22.12+):

```bash
cd final-project/backend
uv sync --locked --group dev
uv run uvicorn app.main:app --reload
```

```bash
cd final-project/frontend
npm ci
npm run dev
```

Frontend: http://localhost:5173. API/Swagger: http://localhost:8000/docs.

Docker commands, from `final-project/`: `docker compose up --build -d`,
`docker compose logs -f`, and `docker compose down`. Node 22 and explicit frontend
build-time values target the local backend at the root asset path. Both images built and all three services became healthy; local API, HTML, and
asset requests returned HTTP 200. Browser CRUD/persistence was not tested. Avoid
deleting volumes when checking persistence; see [deployment.md](docs/deployment.md).

## Test and demonstrate

From `backend/`: `uv run pytest -q`. From `frontend/`: `npm run test:ci` and
`npm run build`. The [testing guide](docs/testing.md) describes installation,
API/integration selections, and the nine frontend core tests.

Demo: view tasks, create a synthetic task, edit it, change status, reload to
confirm persistence, delete it, and reload to confirm removal.

## Deployment and documentation

Read-only HTTP checks returned 200 for the frontend and backend `/tasks` on
2026-10-06. Browser CRUD/persistence and provider settings were not reverified:

- [Frontend](https://stefleur.github.io/kinufaktur-ai-chief-of-staff/)
- [Backend Swagger](https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev/docs)

- [Product specification](product-spec.md)
- [Project instructions](AGENTS.md)
- [API contract](openapi.yaml)
- [AI development evidence](docs/ai-development-workflow.md)
- [Testing](docs/testing.md)
- [Deployment and relocation checklist](docs/deployment.md)
- [Release process](docs/release-process.md)
- [Verbatim draft rubric](docs/final-project-rubric.md)

The future agent extension directories (`agent-capabilities/`, `agent-hooks/`,
`custom-agent/`, `mcp-server/`) belong here in Batch 4. `security/` and `ops/`
belong here in Batch 5. They are not created until real artifacts exist.
