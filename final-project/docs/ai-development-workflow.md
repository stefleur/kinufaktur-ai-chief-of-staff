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
