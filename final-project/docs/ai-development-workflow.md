# AI-assisted development workflow

## Actual planning and human review

The human delegated repository/rubric analysis and a lean implementation plan to
Codex. Context included `final_project_readme.md`, the KinuFlow specification and
OpenAPI contract, source/tests, project instructions, and deployment docs.
The rubric was initially empty; Codex marked scoring unknown and reread it once
the human saved the draft, whose maximum is 30 points.

Codex's first plan proposed broader engineering work. Human review explicitly
removed runtime AI, authentication, migrations, PostgreSQL test infrastructure,
Playwright/E2E, and enterprise observability. The original Batch 1/2 scope kept KinuFlow
under `homework2/` (historical location; superseded by the relocation below), uses synthetic data, preserves Django coursework and existing
hosting, and uses the rubric as the source of truth.

Representative actual instructions supplied by the human:

> MAXIMUM RUBRIC COVERAGE with MINIMUM REASONABLE IMPLEMENTATION COMPLEXITY.

> Start with BATCH 1 + BATCH 2 ONLY.

The human authorized documentation, frontend core tests, small integration-test
cleanup, and creation of `feature/final-project`. No commits, pushes, deployments,
or later batches were authorized. No specialist/subagent has been invoked in
these batches; that component is planned for Batch 4.

## Review and verification procedure

Codex inspects the diff, runs frontend tests/build and backend API/integration
tests, diagnoses failures, and records actual results below. The human reviews
the resulting diff and results before authorizing subsequent work. Implementation
Batches 1/2 were approved by the human from a functional perspective before
relocation; review of this restructuring is pending.

## Evidence log

### 2026-10-06 — Batches 1/2

- Baseline: `7033fd4`; implementation branch: `feature/final-project`.
- Existing untracked `final_project_readme.md` preserved without edits.
- Delegated task: clarify identity and add the approved small frontend test
  suite plus isolated backend integration fixture.
- Files: root README/product spec; KinuFlow README/instructions/testing guide;
  frontend package/lock/config, setup and three test files; backend pytest
  configuration and existing integration test; this evidence log.
- Verification environment: Node v26.5.0, npm 11.17.0, backend Python 3.11;
  newly added packages locked in `frontend/package-lock.json`.
- `uv sync --locked --group dev`: passed (55 packages resolved, 51 checked).
- `npm run test:ci`: 3 files passed, 9 tests passed.
- `npm run build`: passed with Vite 7.3.6, 36 modules transformed.
- `uv run pytest -q -m "not integration"`: 12 passed, 1 deselected.
- `uv run pytest -q -m integration`: 1 passed, 12 deselected.
- `uv run pytest -q`: 13 passed.
- `git diff --check`: passed after implementation and evidence updates.
- Backend runs emit two dependency deprecation warnings (Starlette/httpx and
  anyio BlockingPortal); no dependency upgrade was made.
- npm reported a transitive whatwg-encoding deprecation and install-script
  notices; tests and build passed without additional script approval.
- Initial sandbox attempts blocked Git ref writes, uv cache access, and npm
  registry DNS. Authorized escalation allowed branch creation, sync, install,
  and backend tests to complete. These were environment failures, not test failures.
- Corrections: removed stale prototype instructions, corrected test-command
  working directories and the API-test description, registered the integration
  marker, and replaced leaking database globals with a restoring fixture and
  guaranteed teardown. No test failed and no application behavior was changed.
- Codex reviewed the changes against the authorized file scope; Docker, CI/CD,
  deployment settings, API implementation, and Django code remain untouched.
- Human review: Batches 1/2 functionally approved in the subsequent request.
  No commit or PR is claimed.

Later entries should include the actual task/prompt, context files, reviewed diff,
human decision, commands/results, corrections, and commit/PR references when they
exist. Do not reconstruct fictional development history.

### 2026-10-06 — Canonical Final Project directory

- Human request: make `final-project/` the single canonical product directory,
  move rather than duplicate, preserve verified Batches 1/2 and Django coursework,
  and stop before Batch 3.
- Supersedes the earlier instruction to retain the application under `homework2/`.
- Used `git mv homework2 final-project` to preserve tracked file identity. The
  move also carried untracked Batch 2 tests and ignored local build environments.
- Moved the API contract to `openapi.yaml`, consolidated the original detailed
  specification and root scope pointer into `product-spec.md`, moved AI evidence
  into `docs/`, and moved the rubric verbatim to `docs/final-project-rubric.md`.
- Root README now routes reviewers here and identifies historical Django work.
- Workflow edits only replace `homework2/` paths with `final-project/`; no Node,
  Docker, CI/CD gating, provider, product, or dependency redesign was performed.
- Remaining old paths in prior evidence are HISTORICAL; the old backend provider
  path in the deployment checklist is a HISTORICAL setting to inspect before release.
- Verification from the new locations: `npm ci` passed, frontend `npm run test:ci`
  passed all 9 tests across 3 files, and `npm run build` passed (Vite 7.3.6,
  36 transformed modules). Backend locked sync passed; API selection passed
  12 tests and integration selection passed 1 test in the locked Python 3.11 environment.
- Relocation correction: the moved virtual environment retained absolute pytest
  launcher paths pointing to the historical directory. Initial test invocations
  resolved a system pytest rather than the intended locked environment; their
  results were not used as final evidence. `uv sync --locked --group dev --reinstall`
  refreshed the same 51 locked packages and corrected launcher paths. Backend
  verification was rerun in the intended environment; no lockfile changed.
- Content-hash verification confirmed application source, Batch 2 tests/config,
  both lockfiles, Dockerfiles/Compose, and OpenAPI were preserved exactly.
  Historical Django code/root Python files and rubric bytes were also preserved.
- Markdown links resolve; one frontend/backend remains; package/lock root
  dependencies match. Workflow comparison confirms path substitutions only.
- Full backend suite: 13 passed, with the same two dependency deprecation
  warnings. `git diff --check` and `git diff --cached --check` passed.
  npm emitted the previously seen deprecation/install-script notices; no test
  failure or dependency-version change occurred.
- Human review of restructuring: pending. No commit, push, or deployment.

### 2026-10-06 — Batch 3 lean DevOps

- Human reported PR #4 merged and authorized Batch 3 only, with no commit, push,
  PR creation, provider changes, production deployment, or later-batch work.
- Fast-forwarded main to `fc6f9f7` and confirmed the foundation commit is contained
  in main; created `feature/final-project-devops` from a clean baseline. The old
  local feature branch was retained; no remote branch was deleted.
- Audited actual Dockerfiles/Compose, Vite/client settings, lockfiles, CI/CD,
  and documentation. Fixed Node 18 incompatibility, build-time frontend settings,
  asset base, unlocked backend installation, and the malformed health command.
- CI retains backend tests and frontend build, adds frontend tests, uses Node 22,
  and exposes `workflow_call`; Pages requires successful reusable checks.
  Backend deployment remains external; its manual gating step is documented.
- `npm ci`, `npm run test:ci` (9 passed), default `npm run build`, `uv sync --locked`,
  and `uv run pytest -q` (13 passed) succeeded. A second frontend build using
  `VITE_API_BASE_URL=http://localhost:8000 VITE_BASE=/` succeeded; generated HTML
  uses root assets and compiled JS targets the local backend rather than production.
- Compose config validation, workflow YAML/dependency checks, documentation links,
  and `git diff --check` passed. The revised GitHub workflows have not run remotely.
- Docker daemon socket was absent: no images built, containers started, or local
  HTTP request performed. Runtime container reproducibility is not claimed.
- Read-only production frontend and `/tasks` requests returned HTTP 200; no task
  bodies were saved, and no production data was created/modified. Neon configuration
  and browser persistence were not verified.
- Correction: an initial `npm ci` invocation used the repository root and failed
  for lack of a root package lock; reran successfully from `final-project/frontend`.
  No package or lockfile changed. Existing dependency warnings remain.
- Human review of Batch 3 is pending. Changes remain unstaged/uncommitted.

### 2026-10-06 — Batch 3 container verification follow-up

- The human resent the same Batch 3 request. Preserved all existing work on
  `feature/final-project-devops` rather than restarting or switching branches.
- Docker was now available (server 29.8.0). Built both images and started the
  existing Compose stack with `up --build -d`. All three services became healthy.
- Local backend `/tasks`, frontend HTML, and served JS/CSS returned HTTP 200;
  frontend HTML uses root assets and its JS embeds localhost:8000 rather than
  the production API. No browser CRUD/restart persistence test was performed.
- One frontend request ran before startup completed; subsequent sandbox local
  requests were blocked despite healthy containers. Repeated after startup with
  authorized network access and all required HTTP checks passed.
- `down` stopped/removed the test containers/network without deleting the volume.
  Updated README/testing/deployment evidence to supersede the prior runtime limitation.
- Reran `npm ci`, frontend tests (9 passed), production build, `uv sync --locked`,
  and full backend tests (13 passed). Dependency locks remained unchanged.
- Docker's npm install reported four vulnerability advisories, including two
  critical. Recorded them for security review without installing scanners or
  changing dependencies in this batch. Existing deprecation warnings remain.
- Backend provider gating and actual remote execution of the revised Pages
  workflow remain unverified; no provider settings or production deployment changed.
- No commit, push, PR, merge, or Batch 4 work. Human review remains pending.

### 2026-10-06 — Batch 3 persistence and backend gate preparation

- Human authorized the remaining local runtime/persistence check and safe backend
  workflow preparation only. Preserved the existing branch and uncommitted work.
- `up --build -d` succeeded; PostgreSQL, backend, and frontend were healthy.
  Local frontend `/` and backend `/tasks` returned 200.
- Created one unique synthetic local task (201), confirmed it in the list,
  restarted only backend/frontend, and confirmed the exact record persisted.
  Deleted it (200); its GET returned 404. Stopped with `down` without volume
  deletion, confirmed no containers remained and `final-project_db_data` existed.
  No runtime correction was required; no production data was modified.
- Inspected the existing workflows, installed locked CLI source, and official
  FastAPI Cloud token/CLI/application-directory/GitHub integration documentation.
  Prepared a backend job requiring successful reusable CI and explicit owner
  opt-in (`FASTAPI_CLOUD_DEPLOY_ENABLED=true`). Missing credentials stop it before
  deployment. Default remains disabled; no deployment command was executed.
- Exact secrets are `FASTAPI_CLOUD_TOKEN` and `FASTAPI_CLOUD_APP_ID` for the
  existing app. The CLI uploads the repository root from the backend directory
  with `uv run --locked fastapi deploy ../..`; the owner's Application Directory
  must be `final-project/backend`. Existing provider auto-deploy must be
  disconnected after the Actions path is verified to remove its CI bypass.
- No provider settings or credentials were inspected or changed. Full backend
  gating and remote workflow execution remain unverified. Human review pending.
- No commit, push, PR, merge, production deployment, or Batch 4 work.
- Final regression: 9 frontend tests and production build passed; 13 backend
  tests passed with the same two dependency warnings. YAML/dependency assertions
  and deployment-step shell syntax passed. With both credential variables unset,
  the extracted step failed before invoking the CLI, as intended.
  `git diff --check` passed; changes remain unstaged/uncommitted.
