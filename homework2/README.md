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

