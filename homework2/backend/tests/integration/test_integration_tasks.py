from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import database
from app.database import Base
from app.main import create_app


TASK_INPUT = {
    "title": "Automate invoice intake",
    "description": "Map the current invoice workflow.",
    "category": "AI Automation",
    "priority": "High",
    "status": "incoming",
}


def create_task(client, **changes):
    payload = {**TASK_INPUT, **changes}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def test_full_task_lifecycle_uses_real_persistence():
    # Use a dedicated in-memory SQLite engine with StaticPool so the
    # TestClient (which runs the app in a different thread) can reuse
    # the same connection. This replaces the module-level engine and
    # SessionLocal so the app uses a test database without mocking.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    database.engine = engine
    database.SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    # Create tables against the test engine and start the real app.
    Base.metadata.create_all(bind=engine)
    test_app = create_app(initialize_database=True)

    with TestClient(test_app) as client:
        # Create
        task = create_task(client)
        task_id = task["id"]

        # List
        resp = client.get("/tasks")
        assert resp.status_code == 200
        assert any(t["id"] == task_id for t in resp.json())

        # Get
        resp = client.get(f"/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == task_id

        # Update (title)
        resp = client.patch(f"/tasks/{task_id}", json={"title": "New title"})
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["title"] == "New title"
        assert updated["created_at"] == task["created_at"]

        # Change status
        resp = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "in_progress"

        # Delete
        resp = client.delete(f"/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json() == {"id": task_id}

        # Verify persistence (deleted)
        assert client.get(f"/tasks/{task_id}").status_code == 404

    # Teardown
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
