# KinuFlow

KinuFlow is a Mini Kanban Board created for the DataTalksClub AI Dev Tools Zoomcamp 2026.

It is designed as an internal operations board for Kinufaktur.

## Planned Stack

- React frontend
- FastAPI backend
- SQLAlchemy
- Python with uv
- Node.js

## Local Docker & Docker Compose workflow

Build images (from `agent1/homework2`):

```bash
cd agent1/homework2
docker compose build
```

Start stack (detached):

```bash
cd agent1/homework2
docker compose up -d
```

Stop and remove containers:

```bash
cd agent1/homework2
docker compose down
```

Rebuild images and restart:

```bash
cd agent1/homework2
docker compose build --no-cache
docker compose up -d
```

View logs:

```bash
cd agent1/homework2
docker compose logs -f
```

Run tests (backend):

```bash
cd agent1/homework2/backend
# run all tests
pytest -q

# run only integration tests
pytest -q -m integration

# run non-integration tests
pytest -q -m "not integration"
```

Local URLs:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Production

- Frontend: [https://stefleur.github.io/kinufaktur-ai-chief-of-staff/](https://stefleur.github.io/kinufaktur-ai-chief-of-staff/)
- Backend API documentation: [https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev/docs](https://kinufaktur-ai-chief-of-staff-89a42968.fastapicloud.dev/docs)

The production architecture is a React frontend hosted on GitHub Pages, a FastAPI backend hosted on FastAPI Cloud, and a Neon PostgreSQL database:

```text
GitHub Pages -> FastAPI Cloud -> Neon PostgreSQL
```

GitHub Actions runs CI through `.github/workflows/ci.yml`. Changes on `main` automatically deploy the frontend through `.github/workflows/deploy.yml`, while FastAPI Cloud's GitHub integration automatically deploys backend changes.

## Documentation

- [Testing](docs/testing.md)
- [Production deployment](docs/deployment.md)
- [Release process](docs/release-process.md)
