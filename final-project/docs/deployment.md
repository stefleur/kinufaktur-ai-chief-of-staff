# KinuFlow deployment

## Production architecture

```text
GitHub Pages frontend -> FastAPI Cloud backend -> Neon PostgreSQL
```

- [Frontend](https://stefleur.github.io/kinufaktur-ai-chief-of-staff/)
- [Backend](https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev)
- [Backend Swagger](https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev/docs)

The existing providers, URLs, secrets, and database schema are preserved. Batch 3
changes are local and uncommitted; no production deployment was requested.

## Local development

From the repository root, in separate terminals:

```bash
cd final-project/backend
uv sync --locked
uv run uvicorn app.main:app --reload
```

```bash
cd final-project/frontend
npm ci
npm run dev
```

Use Node compatible with locked Vite 7 (20.19+ or 22.12+); Docker and CI use Node 22.
The backend defaults to SQLite. Frontend development defaults to localhost:8000.
See [testing.md](testing.md) for tests. Use synthetic/demo data only.

## Local Docker Compose

From the repository root:

```bash
docker compose -f final-project/docker-compose.yml config
docker compose -f final-project/docker-compose.yml up --build -d
docker compose -f final-project/docker-compose.yml ps
curl --fail http://localhost:8000/tasks
curl --fail http://localhost:5173/
docker compose -f final-project/docker-compose.yml logs backend
```

The frontend is at localhost:5173; backend/Swagger is at localhost:8000/docs.
Compose builds the frontend with `VITE_API_BASE_URL=http://localhost:8000` and
`VITE_BASE=/`. These are build-time values: changing them requires rebuilding.
The browser connects to the exposed backend; it cannot use the internal Docker
hostname. The backend connects to PostgreSQL at the Compose service `postgres`.
Database data lives in a named volume; `docker compose down` retains it.

Stop the stack cleanly after checks:

```bash
docker compose -f final-project/docker-compose.yml down
```

Do not use `down -v` when verifying persistence. Compose's fixed credentials are
local demo defaults only, not production credentials. Startup waits for PostgreSQL
and then backend `/tasks` checks; no additional health endpoints are introduced.
The backend image installs runtime dependencies from `uv.lock` with pinned uv
0.12.23; the frontend uses `npm ci`. Base image tags still receive upstream patches;
this is locked dependency installation, not a bit-identical image guarantee.

## Environment configuration

| Variable | Location and behavior |
|---|---|
| `VITE_API_BASE_URL` | Preferred public frontend API URL; Docker build argument embedded into JS |
| `VITE_API_BASE` | Existing frontend compatibility variable; Pages workflow preserves `vars.VITE_API_BASE` |
| `VITE_BASE` | Public asset base at build time; Compose `/`; Pages defaults to `/kinufaktur-ai-chief-of-staff/` and accepts existing `vars.VITE_BASE` |
| `DATABASE_URL` | Backend production secret for Neon; takes precedence over the project-specific URL |
| `KINUFLOW_DATABASE_URL` | Backend fallback; Compose PostgreSQL URL, otherwise SQLite default |
| `KINUFLOW_CORS_ORIGINS` | Comma-separated backend origin allowlist; production should include `https://stefleur.github.io`; local defaults include localhost:5173 |
| `PORT` | Optional backend listener port; defaults to 8000 |

Frontend variables are public configuration, never secret storage. Keep real
connection strings/tokens in provider secret settings; never commit or print them.
Existing Neon and CORS settings are described by earlier documentation, not
independently inspected in Batch 3.

## CI and GitHub Pages gating

[CI](../../.github/workflows/ci.yml) runs on PRs to main and pushes to main. It
installs locked Python dependencies and runs the backend suite; frontend checks
run `npm ci`, `npm run test:ci`, and `npm run build` on Node 22.

The [Pages workflow](../../.github/workflows/deploy.yml) runs on pushes to main.
Its `checks` job calls the same CI workflow through `workflow_call`. The Pages
build/deploy job requires `checks` to succeed; a failed check skips deployment.
It checks out the same event commit, preserves the existing repository variables,
and publishes the existing GitHub Pages site. PR checks do not deploy.
This simple reuse reruns verification on main rather than introducing a new
release platform. The changed workflow has not yet run on GitHub because it has
not been committed or pushed.

## External FastAPI Cloud deployment and remaining manual step

The repository now prepares a `deploy_backend` job with `needs: checks`, so its
CLI deployment can only run after the reusable CI succeeds for the same commit.
It is **disabled by default**: the repository Actions variable
`FASTAPI_CLOUD_DEPLOY_ENABLED` must equal `true`. Missing secrets fail the enabled
job before deployment; the existing Pages job remains independently gated by CI.
No provider settings, credentials, or production deployments were changed.

Repository code alone cannot complete gating: the existing FastAPI Cloud GitHub
integration deploys on default-branch pushes independently of Actions. Its actual
configuration has not been inspected through the owner's dashboard.

The smallest remaining owner configuration is:

1. In the **existing app**, verify Application Directory is
   `final-project/backend`; correct a historical directory only during the
   authorized owner cutover. Keep the existing app, URL, Neon, and CORS settings.
2. Use an existing app-scoped deploy token, or obtain one through that app's
   **Deploy Tokens** page. Copy the existing app's full UUID from its dashboard
   header; the URL slug is not the app ID.
3. Add repository Actions secrets `FASTAPI_CLOUD_TOKEN` (app-scoped token) and
   `FASTAPI_CLOUD_APP_ID` (that existing app UUID). No Neon secret is needed in
   GitHub: database configuration stays with the existing provider app.
4. After this workflow is reviewed and delivered, set the repository Actions
   variable `FASTAPI_CLOUD_DEPLOY_ENABLED=true` for the authorized release and
   verify its backend deployment succeeds after `checks`.
5. Once the Actions deployment path is verified, disconnect the existing app's
   GitHub source in **Settings -> Source Repository**. This disables the separate
   auto-deploy trigger and keeps the existing deployment running. Until this is
   done, pushes can bypass the CI gate; do not claim full gating during cutover.

The exact prepared command, from `final-project/backend`, is:

```bash
uv run --locked fastapi deploy ../..
```

`FASTAPI_CLOUD_TOKEN` and `FASTAPI_CLOUD_APP_ID` are supplied by the deployment
step. The command uploads the repository root, matching the app's nested
Application Directory, and waits for deployment verification. The existing
lockfile already includes `fastapi-cloud-cli` 0.26.0; no new dependency or local
cloud linkage is necessary. No deploy command was executed in this batch.

Official references: [deploy tokens and GitHub secret names](https://fastapicloud.com/docs/advanced-features/deploy-tokens/),
[CLI path and app selection](https://fastapicloud.com/docs/fastapi-cloud-cli/deploy/),
[application directory](https://fastapicloud.com/docs/builds-and-deployments/application-directory/),
and [disconnecting GitHub integration](https://fastapicloud.com/docs/source-control/github-integration/).

## Deployment verification and Batch 3 evidence

Read-only HTTP checks on 2026-10-06 returned **200** for the production frontend
and backend `GET /tasks`. This establishes reachable deployed URLs; it does not
prove browser CRUD, Neon settings, or restart persistence. No task response data
was saved, and no production task was created or modified.

After an authorized release, check the frontend, API, and Swagger. Use a uniquely
named synthetic task to create/edit/move/reload/delete and confirm persistence.
Record actual results; do not infer database persistence from a single HTTP 200.

Local Compose configuration validates. Docker Desktop was unavailable on the
first attempt, then available on the follow-up. `up --build -d` built both images
and started all three services; PostgreSQL, backend, and frontend reported healthy.
Local `/tasks`, frontend HTML, JavaScript, and CSS returned HTTP 200. The served JS
embeds localhost:8000 and the HTML uses root asset paths. `down` stopped/removed
the test containers and network while retaining the database volume. These initial
checks did not exercise browser CRUD or restart persistence.

The Docker frontend install reported four npm vulnerability advisories (one
moderate, one high, two critical). Their individual findings were not investigated
in this batch and no dependency changes were made; review them during the planned
security work. Builds and regression tests passed.

The app retains SQLAlchemy table creation; no schema change or migration system
was introduced.

### 2026-10-06 — Local API persistence verification

A subsequent `up --build -d` succeeded. All three services reported healthy;
`GET http://localhost:8000/tasks` and `GET http://localhost:5173/` returned 200.
Created one uniquely named synthetic local task (POST 201), confirmed the exact
record in `GET /tasks`, restarted only `backend frontend`, and confirmed that
same record (including its ID and timestamps) remained in `GET /tasks` (200).
Deleted the synthetic task (200); its individual GET then returned 404.
No runtime corrections were required. `down` stopped/removed the stack without
volume deletion; `ps -a` was empty and `final-project_db_data` still existed.
This is local API/PostgreSQL restart evidence, not a browser or Neon test.
