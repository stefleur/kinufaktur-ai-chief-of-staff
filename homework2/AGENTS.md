# AGENTS.md

## Project

This project is called KinuFlow.

It is a Mini Kanban Board for the DataTalksClub AI Dev Tools Zoomcamp.

Always read `_docs/specs.md` before making architectural changes.

## Development Principles

- Keep the implementation simple.
- Do not add features outside the specification unless requested.
- Prefer readable code.
- Do not commit secrets or API keys.

## Frontend

- Centralize backend/API calls in one module.
- Use mocked API responses first.
- Keep components small and understandable.

## Backend

- Use FastAPI.
- Use uv for Python dependency management.
- Write tests for endpoints.
- Keep persistence behind a separate data-access layer.

## Database

- Use SQLAlchemy when introducing the real database.
- Avoid coupling application logic directly to one database.

## Testing

Run relevant tests before considering a task complete.
