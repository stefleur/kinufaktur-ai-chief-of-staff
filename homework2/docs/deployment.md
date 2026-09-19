# Production deployment

## Architecture

The production request flow is:

```text
GitHub Pages frontend -> FastAPI Cloud backend -> Neon PostgreSQL
```

- Frontend: [https://stefleur.github.io/kinufaktur-ai-chief-of-staff/](https://stefleur.github.io/kinufaktur-ai-chief-of-staff/)
- Backend: [https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev](https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev)
- Database: Neon PostgreSQL

## Production configuration

The backend is configured in FastAPI Cloud with these environment variables:

- `DATABASE_URL` is set as a secret containing the Neon PostgreSQL connection URL.
- `KINUFLOW_CORS_ORIGINS` is set to `https://stefleur.github.io` so the GitHub Pages frontend can call the API.

Passwords and database connection strings must not be committed to the repository or included in documentation.

## Deployment automation

Frontend deployment happens automatically from `main` through GitHub Actions using `.github/workflows/deploy.yml`. The workflow builds the Vite frontend and publishes it to GitHub Pages.

Backend deployment happens automatically through FastAPI Cloud's GitHub integration. Backend changes pushed to the connected GitHub repository are redeployed by FastAPI Cloud.

Continuous integration runs through `.github/workflows/ci.yml`.

## Production smoke test

After a deployment:

1. Send `GET /tasks` to the production backend and verify that it returns a successful response:

   ```bash
   curl --fail https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev/tasks
   ```

2. Open the [production frontend](https://stefleur.github.io/kinufaktur-ai-chief-of-staff/) and create a task.
3. Reload the page and verify that the task is still present, confirming persistence in Neon PostgreSQL.

## Known database migration limitation

The current application uses SQLAlchemy table creation rather than a formal Alembic migration workflow. Production schema migrations are therefore a known limitation and a future improvement.
